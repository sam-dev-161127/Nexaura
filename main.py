import speech_recognition as sr       # Converts microphone voice into text | pip install SpeechRecognition
import os                             # Used for file handling, opening apps, folders, songs, etc.
import glob
import re                             # Used for pattern matching and cleaning text commands
import webbrowser                     # Opens websites directly in the default browser
import datetime                       # Gives current date, time, day, month, year, etc.
# Gemini AI integration (imported dynamically later to prefer google.genai)
import config                         # Stores secret data like API keys separately
import random                         # Used for random replies, songs, jokes, choices, etc.
import threading                      # Runs multiple tasks at the same time (multitasking)
import win32com.client                # Windows built-in text to speech | pip install pywin32

# ----------------------------------#
#   Nexaura - voice assistant       #
#          main script              #
#                                   #
# Purpose:                          #
# - Listen to microphone commands   #
#   and perform actions on Windows: #
#   • open websites                 #
#   • launch desktop apps from a    #
#     shortcut folder               #
#   • simple AI chat using Google   #
#     Gemini (configured via        #
#     config.API_KEY)               #
#                                   #
# Key features & usage notes:       #
# - Place your application          #
#   shortcuts (.lnk) in the folder  #
#   configured by SHORTCUT_FOLDER   #
#   (default: Shourtcut/Shortcut    #
#   under the project). The         #
#   assistant maps shortcut         #
#   filenames (without .lnk) to     #
#   spoken app names.               #
# - Voice commands examples:        #
#   • "open telegram" → launches    #
#     telegram.lnk if present in    #
#     the shortcuts folder          #
#   • "enable ai" / "disable ai"    #
#     → toggles Gemini AI           #
#     conversation mode             #
#   • "stop" → immediately          #
#     interrupts ongoing speech     #
#   • "clear chat" → clears stored  #
#     AI conversation memory        #
# - Songs/games static lists were   #
#   removed. Use the shortcuts      #
#   folder to manage apps/games or  #
#   ask me to re-add a dedicated    #
#   music/game handler.             #
# - The code currently imports      #
#   `google.generativeai` (legacy); #
#   migrating to `google.genai` is  #
#   recommended. Store your API key #
#   in `config.py` as               #
#   `API_KEY = "your-key"` before   #
#   enabling AI features.           #
#                                   #
# Running:                          #
#   python main.py                  #
#                                   #
# Notes for maintainers:            #
# - The assistant uses SAPI via     #
#   win32com for TTS (Windows only).#
# - Shortcut name matching is       #
#   case-insensitive and uses simple#
#   substring matching; consider    #
#   adding synonyms or fuzzy        #
#   matching for better UX.         #
# ----------------------------------#


# ----------------------------------#
#       Text-to-Speech (TTS)        #
# Uses Windows SAPI via win32com    #
# to perform speech output.         #
# This is Windows-only;             #
# `speaker.Speak(text, flags)`      #
# is used throughout.               #
# For cross-platform TTS consider   #
# pyttsx3 or other libraries.       #
# ----------------------------------#
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# flag to cancel speaking mid-sentence
is_speaking = False

# flag to stop current AI speech instantly
stop_requested = False

# ----------------------------------#
#       store chat history          #
# stores previous conversation      #
# between user and Nexaura          #
# helps AI remember conversation    #
# context                           #
#                                   #
# example:                          #
# Sam: hello                        #
# Nexaura: hi                       #
# ----------------------------------#
chatStr = ""

# ----------------------------------#
#       AI mode toggle              #
# Primary Mode  -> AI Enabled       #
#   (Gemini AI conversation mode)   #
# Secondary Mode -> AI Disabled     #
#   (Normal command execution mode) #
# False → normal assistant mode     #
# True  → AI conversation mode      #
# voice commands:                   #
# "enable ai"                       #
# "disable ai"                      #
# ----------------------------------#
ai_enabled = False

# Configure Gemini API (prefer new `google.genai`, fallback to legacy)
try:
    # preferred (new package)
    import google.genai as genai
    NEW_GENAI = True
except Exception:
    # google.genai not available. Do NOT import the deprecated
    # google.generativeai to avoid FutureWarnings. Disable AI features and
    # instruct the user to install the new package.
    genai = None
    NEW_GENAI = False
    print("google.genai not installed — AI features disabled. To enable, run: python -m pip install --upgrade google-genai")

# Try to configure/authenticate. New SDKs may expose a Client or Model API.
client = None
model = None
# Prefer calling configure() if available
if hasattr(genai, "configure"):
    try:
        genai.configure(api_key=config.API_KEY)
    except Exception as e:
        print("genai.configure error:", e)

# If the module exposes a Client class, create one (new SDKs may do this)
if hasattr(genai, "Client"):
    try:
        client = genai.Client(api_key=config.API_KEY)
    except Exception:
        client = None

# If the new SDK exposes a Model class, try to create it
if NEW_GENAI and hasattr(genai, "Model"):
    try:
        # some genai variants use Model(model_name=...)
        model = genai.Model(model_name="gemini-2.5-flash")
    except Exception:
        model = None

# Legacy style: create GenerativeModel if available in older package
if (not NEW_GENAI) and hasattr(genai, "GenerativeModel"):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        print("GenerativeModel creation error:", e)
        model = None


# ----------------------------------#
#     GenAI runtime diagnostic      #
# Prints which backend was selected #
# and which APIs are available.     #
# ----------------------------------#
try:
    backend = "google.genai" if NEW_GENAI else "google.generativeai"
    available = []
    for attr in ("configure", "Client", "Model", "GenerativeModel", "generate_text", "generate", "get_model"):
        if hasattr(genai, attr):
            available.append(attr)
    print(f"GenAI backend: {backend}; available: {', '.join(available) if available else 'none'}")
    if client is not None:
        print("GenAI client: created")
    if model is not None:
        print(f"GenAI model: created ({type(model).__name__})")
except Exception as e:
    print("GenAI diagnostic error:", e)

# Compatibility wrapper exposing generate_content(prompt) → object with .text
class _SimpleResp:
    def __init__(self, text):
        self.text = text


def _extract_text(resp):
    # Try common shapes safely
    if resp is None:
        return None
    # object with text attribute
    if hasattr(resp, "text") and isinstance(getattr(resp, "text"), str):
        return resp.text
    # generations list
    if hasattr(resp, "generations"):
        gen = getattr(resp, "generations")
        try:
            return gen[0].text
        except Exception:
            pass
    # outputs / candidates (dict-like)
    try:
        if isinstance(resp, dict):
            if "candidates" in resp and resp["candidates"]:
                c = resp["candidates"][0]
                return c.get("content") or c.get("text")
            if "outputs" in resp and resp["outputs"]:
                out = resp["outputs"][0]
                if isinstance(out, dict):
                    return out.get("content") or out.get("text")
    except Exception:
        pass
    # fallback to string conversion
    try:
        return str(resp)
    except Exception:
        return None


class GenAICompat:
    def __init__(self, genai_module, client_obj=None, model_obj=None, model_name="gemini-2.5-flash"):
        self.genai = genai_module
        self.client = client_obj
        self.model = model_obj
        self.model_name = model_name

    def generate_content(self, prompt):
        # 1) legacy model.generate_content
        try:
            if self.model is not None and hasattr(self.model, "generate_content"):
                resp = self.model.generate_content(prompt)
                text = _extract_text(resp)
                return _SimpleResp(text or "")
        except Exception as e:
            print("model.generate_content error:", e)

        # 2) module-level generate_text / generate
        try:
            if hasattr(self.genai, "generate_text"):
                resp = self.genai.generate_text(input=prompt, model=self.model_name)
                text = _extract_text(resp)
                return _SimpleResp(text or "")
        except Exception:
            pass

        # 3) client-based generate_text
        try:
            if self.client is not None and hasattr(self.client, "generate_text"):
                resp = self.client.generate_text(input=prompt, model=self.model_name)
                text = _extract_text(resp)
                return _SimpleResp(text or "")
        except Exception:
            pass

        # 4) last resort: return empty response
        return _SimpleResp("")


# Replace raw model with compatibility wrapper
model = GenAICompat(genai, client_obj=client, model_obj=model)


# ----------------------------------#
#       Clean AI Response           #
# clean_for_speech(text):           #
# - Strips markdown, code blocks,   #
#   links and excessive whitespace  #
# - Returns a short, natural-       #
#   sounding string suitable for    #
#   TTS                             #
# ----------------------------------#
def clean_for_speech(text):

    # remove bold and italic markdown
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)

    # remove markdown headings
    text = re.sub(r'#{1,6}\s*', '', text)

    # remove inline and multiline code blocks
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)

    # remove markdown links but keep visible text (non-regex fallback to avoid linter warnings)
    def _strip_md_links(s):
        out_parts = []
        i = 0
        while True:
            start = s.find('[', i)
            if start == -1:
                break
            mid = s.find('](', start)
            if mid == -1:
                break
            end = s.find(')', mid)
            if end == -1:
                break
            # append text before [, then visible text inside [..]
            out_parts.append(s[i:start])
            out_parts.append(s[start+1:mid])
            i = end+1
        out_parts.append(s[i:])
        return ''.join(out_parts)

    text = _strip_md_links(text)

    # remove bullet points
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)

    # replace multiple lines with single space
    text = re.sub(r'\n+', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


# ----------------------------------#
#       Speak (blocking)            #
# sayAndWait(text): speak the given #
# text and BLOCK until speech       #
# finishes. Use this before actions #
# like opening apps or launching    #
# websites so the assistant         #
# finishes talking before           #
# performing the action.            #
# ----------------------------------#
def sayAndWait(text):
    global is_speaking
    global stop_requested

    text = clean_for_speech(text)

    # do not speak if stop was requested
    if stop_requested:
        return

    print("Nexaura :", text)
    is_speaking = True

    # ----------------------------------#
    # split long AI response into       #
    # smaller chunks                    #
    # helps:                            #
    # - smoother speech playback        #
    # - faster stop response            #
    # - prevents long speech freezing   #
    # ----------------------------------#
    sentences = re.split(r'(?<=[.!?]) +', text)

    for sentence in sentences:

        # instantly stop if user says stop
        if stop_requested:

            # ----------------------------------#
            # SVSFPurgeBeforeSpeak flag = 3     #
            # clears:                           #
            # - current speech                  #
            # - queued speech                   #
            # allows instant interruption       #
            # ----------------------------------#
            speaker.Speak("", 3)
            break

        speaker.Speak(sentence, 0)

    is_speaking = False
    stop_requested = False


# ----------------------------------#
#       Speak (non-blocking)        #
# say(text): starts a background    #
# thread and speaks without         #
# waiting. Use for long AI replies  #
# when you want the program to      #
# continue.                         #
# ----------------------------------#
def say(text):
    threading.Thread(target=sayAndWait, args=(text,), daemon=True).start()


# ----------------------------------#
#    Stop speaking immediately      #
# stopSpeaking(): sets a stop flag  #
# and purges the SAPI queue so      #
# speech halts instantly. Useful    #
# when user says "stop" during AI   #
# reply.                            #
# ----------------------------------#
def stopSpeaking():
    global is_speaking
    global stop_requested

    try:
        stop_requested = True
        is_speaking = False

        # SVSFPurgeBeforeSpeak flag (3) = clear queue and stop current speech instantly
        speaker.Speak("", 3)

        print("Nexaura stopped speaking")

    except Exception as e:
        print("Stop error:", e)


# ----------------------------------#
#    Clear AI conversation memory   #
# clearChat(): Resets the stored    #
# chat history used to provide      #
# context to the AI. Use when AI    #
# responses become irrelevant or    #
# you want a fresh conversation.    #
# ----------------------------------#
def clearChat():
    global chatStr

    chatStr = ""
    sayAndWait("Chat cleared")


# ----------------------------------#
#    AI chat using Gemini           #
# aiChat(query): sends conversation #
# history + query to the Gemini     #
# model and speaks/saves the reply. #
# Requires a working `model` and    #
# `config.API_KEY` configured at    #
# top of file.                      #
# ----------------------------------#
def aiChat(query):
    global chatStr
    global stop_requested

    # reset stop flag before new AI reply
    stop_requested = False

    # store user query into conversation memory
    chatStr += f"Sam: {query}\nNexaura: "

    # send full conversation to Gemini AI
    response = model.generate_content(chatStr)

    reply = response.text

    # store AI reply into memory
    chatStr += f"{reply}\n"

    print(reply)

    # speak AI reply
    say(reply)

    # ----------------------------------#
    # create Gemini folder if not       #
    # present                           #
    # this folder stores all AI         #
    # conversation logs as text files   #
    # you can rename:                   #
    # "Gemini"                          #
    # "Chats"                           #
    # "AI Logs"                         #
    # ----------------------------------#
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # remove unwanted text from filename
    filename = query.replace("using artificial intelligence", "").strip()

    # ----------------------------------#
    # remove invalid Windows filename   #
    # characters                        #
    # Windows does NOT allow:           #
    # \ / : * ? " < > |                 #
    # without cleanup:                  #
    # file saving may fail              #
    # ----------------------------------#
    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    # create random filename if query is empty
    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    # save AI response into text file
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# ----------------------------------#
#   AI control and voice-command    #
#         dispatcher                #
# useAI(query): handles voice       #
# commands related to AI mode:      #
# - "stop" -> interrupts speech     #
# - "enable ai" / "disable ai"      #
#   -> toggle conversation mode     #
# - "clear chat" -> reset AI memory #
# When AI mode is enabled, regular  #
# commands will be sent to aiChat.  #
# ----------------------------------#
def useAI(query):
    global ai_enabled

    # stop Nexaura voice immediately — checked FIRST so it always works
    if "stop" in query:
        stopSpeaking()
        return True

    # enable AI mode
    if "enable ai" in query:
        ai_enabled = True
        sayAndWait("AI enabled")
        return True

    # disable AI mode
    if "disable ai" in query:
        ai_enabled = False
        sayAndWait("AI disabled")
        return True

    # clear stored AI conversation memory
    if "clear chat" in query:
        clearChat()
        return True

    # if AI mode is enabled then use Gemini AI
    if ai_enabled:
        aiChat(query)
        return True

    return False


# ----------------------------------#
#       Microphone selection        #
# get_mic_index(): inspects         #
# connected microphones and returns #
# the index of a likely device      #
# (prefers Realtek or any with      #
# 'microphone' in its name).        #
# Returns None if no suitable       #
# device found.                     #
# ----------------------------------#
def get_mic_index():

    # get all connected microphone names
    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):

        # convert microphone name to lowercase
        # helps detect more Realtek microphone variations
        mic_name = name.lower()

        # ----------------------------------#
        # auto detect Realtek microphones   #
        #                                   #
        # works for:                        #
        # - Realtek HD Audio                #
        # - Realtek(R) Audio                #
        # - Microphone Array                #
        # - laptop microphones              #
        # ----------------------------------#
        if "realtek" in mic_name:
            return i

        # fallback for generic microphone arrays
        if "microphone" in mic_name:
            return i

    return None


# ----------------------------------#
#  Capture voice input and convert  #
#           to text                 #
# takeCommand(): listens on the     #
# selected microphone and returns   #
# the recognized text (lowercased). #
# Configurable parameters in-code:  #
# - energy_threshold,               #
#   dynamic_energy_threshold,       #
#   pause_threshold,                #
# - timeout and phrase_time_limit   #
#   passed to recognizer.listen     #
# ----------------------------------#
def takeCommand():

    # create speech recognizer object
    r = sr.Recognizer()

    # ----------------------------------#
    # Recognizer sensitivity settings   #
    # (tweak if recognition is poor).   #
    # energy_threshold: microphone      #
    # sensitivity (lower = more         #
    # sensitive).                       #
    # dynamic_energy_threshold: when    #
    # True, adjusts automatically.      #
    # pause_threshold: seconds of       #
    # silence that mark end of phrase.  #
    # ----------------------------------#
    r.energy_threshold = 200
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.2

    mic_index = get_mic_index()

    # return empty string if no microphone found
    if mic_index is None:
        print("No microphone found")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            # -----------------------------------#
            # noise calibration duration         #
            # in seconds                         #
            # increase if:                       #
            # - room is noisy                    #
            # - fan/AC noise exists              #
            # decrease if:                       #
            # - room is quiet                    #
            # - you want faster listening        #
            # recommended:                       #
            # 0.5 → quiet room                   #
            # 1.0 → balanced                     #
            # 2.0 → noisy room                   #
            #                                    #
            # 2 seconds recommended for better   #
            # Indian accent recognition accuracy #
            # -----------------------------------#
            r.adjust_for_ambient_noise(source, duration=2)

            print("Listening...")

            # ----------------------------------#
            # Listening timeouts: timeout waits #
            # for user to START speaking;       #
            # phrase_time_limit limits how long #
            # to listen after speech starts.    #
            # Adjust the pair (timeout,         #
            # phrase_time_limit) for your       #
            # environment.                      #
            # ----------------------------------#
            audio = r.listen(source, timeout=5, phrase_time_limit=7)

            print("Recognizing...")

            # ----------------------------------#
            # convert voice into text using     #
            # Google Speech Recognition         #
            # 'en-IN' → Indian English          #
            # 'en-US' → American English        #
            # 'en-GB' → British English         #
            #                                   #
            # en-IN gives best results for:     #
            # - Indian pronunciation            #
            # - Hinglish words                  #
            # - Indian names                    #
            # - mixed Indian English speech     #
            # ----------------------------------#
            query = r.recognize_google(audio, language='en-IN')

            print("User said:", query)

            return query.lower()

    except sr.WaitTimeoutError:
        # triggered when user does not start speaking in time
        print("Listening timeout")
        return ""

    except sr.UnknownValueError:
        # triggered when speech was unclear
        print("Could not understand audio")
        sayAndWait("Sorry Sam, I could not understand")
        return ""

    except Exception as e:
        # catches microphone/device errors
        print("Mic error:", e)
        return ""


# start program
if __name__ == '__main__':
    print("Nexaura started")
    sayAndWait("I am Nexaura AI")

    # ----------------------------------#
    # websites list (you can add more   #
    # sites)                            #
    # format:                           #
    # ["spoken name", "website url"]    #
    # example:                          #
    # saying "open youtube"             #
    # opens youtube website             #
    # ----------------------------------#
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["twitter", "https://www.x.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["amazon", "https://www.amazon.in"],
        ["flipkart", "https://www.flipkart.com"],
        ["netflix", "https://www.netflix.com"],
        ["spotify", "https://www.spotify.com"],
        ["jiohotstar", "https://www.jiohotstar.com"],
        ["code with harry", "https://www.codewithharry.com"],
        ["geeksforgeeks", "https://www.geeksforgeeks.org"],
        ["w3schools", "https://www.w3schools.com"],
        ["leetcode", "https://leetcode.com"],
        ["hackerrank", "https://www.hackerrank.com"],
        ["stackoverflow", "https://stackoverflow.com"],
        ["canva", "https://www.canva.com"],
        ["replit", "https://replit.com"],
        ["coursera", "https://www.coursera.org"],
    ]

    # (songs and games lists removed — using shortcut folder for apps instead)

    # ---------------------------------#
    #   SHORTCUT SCANNER               #
    #   launch desktop apps            #
    # Place .lnk shortcut files in     #
    # SHORTCUT_FOLDER. The assistant   #
    # maps filenames (without .lnk)    #
    # to spoken names.                 #
    # Example: telegram.lnk ->         #
    # "telegram"                       #
    # ---------------------------------#

    SHORTCUT_FOLDER = r"C:\Users\Sam-Dev-161127\PycharmProjects\Nexaura\Shortcut"

    # Dictionary to store shortcuts (spoken name -> shortcut path)
    apps = {}

    # ---------------------------------#
    #         SCAN SHORTCUTS           #
    # ---------------------------------#

    # scan .lnk files
    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.lnk")):
        # Get shortcut name without .lnk and normalize
        app_name = os.path.basename(shortcut).replace(".lnk", "").lower().strip()

        apps[app_name] = shortcut

    # scan .mp3 files
    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.mp3")):
        # Get shortcut name without .mp3 and normalize
        app_name = os.path.basename(shortcut).replace(".mp3", "").lower().strip()

        apps[app_name] = shortcut


    # Loaded shortcuts are available in `apps` dict.

    # ---------------------------------#
    #       CLEAN VOICE COMMAND        #
    # ---------------------------------#
    def clean_command(command):

        remove_words = [
            "open",
            "start",
            "launch",
            "play",
            "please"
        ]

        command = command.lower()

        for word in remove_words:
            command = command.replace(word, "")

        return command.strip()


    # ---------------------------------#
    #       OPEN APP FUNCTION          #
    # ---------------------------------#
    def open_app(command):

        command_clean = clean_command(command)

        print("Cleaned command:", command_clean)


        if command_clean in apps:
            sayAndWait("Opening " + command_clean)

            os.startfile(apps[command_clean])

            return True


        for name in apps:

            # Example:
            # "play believer"
            # matches:
            # "believer imagine dragons"

            if command_clean in name or name in command_clean:
                sayAndWait("Opening " + name)

                os.startfile(apps[name])

                return True

        # ---------------------------------#
        # not found                        #
        # ---------------------------------#
        return False


    # ----------------------------------#
    # infinite loop for continuous      #
    # listening                         #
    # Nexaura keeps running until:      #
    # - terminal is closed              #
    # - program is stopped              #
    # - PC shuts down                   #
    # ----------------------------------#
    while True:

        query = takeCommand()

        # skip loop if nothing was heard
        if query == "":
            continue

        command_matched = False

        # ---------------------------------#
        # handle AI commands first         #
        #                                  #
        # important:                       #
        # AI commands should run before    #
        # normal commands                  #
        # ---------------------------------#
        if useAI(query):
            continue

        # ---------------------------------#
        # open apps / songs                #
        # ---------------------------------#
        if open_app(query):
            continue

        # open websites — sayAndWait so Nexaura finishes speaking before browser opens
        for site in sites:
            if f"open {site[0]}" in query:
                sayAndWait("Opening " + site[0])
                webbrowser.open(site[1])
                command_matched = True
                break  # ← FIX: stop after first match

        # play songs and games handling removed (using shortcut folder for apps)

        # open apps using shortcuts folder
        if any(kw in query for kw in ("open ", "start ", "launch ")):
            if open_app(query):
                command_matched = True

        # ---------------------------------#
        #       tell current time          #
        # ---------------------------------#
        if "what time is it" in query:
            now = datetime.datetime.now()

            # ---------------------------------#
            # time formatting codes            #
            #                                  #
            # %I → hour (12-hour format)       #
            # %H → hour (24-hour format)       #
            # %M → minutes                     #
            # %S → seconds                     #
            # %p → AM/PM                       #
            #                                  #
            # example:                         #
            # 09:45 PM                         #
            # ---------------------------------#
            hour = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm = now.strftime("%p")
            sayAndWait(f"The time is {hour}:{minute} {am_pm}")

            command_matched = True

        # ---------------------------------#
        #       tell current date          #
        # ---------------------------------#
        if "what date is it" in query:
            now = datetime.datetime.now()

            # ---------------------------------#
            # date formatting codes            #
            #                                  #
            # %A → full weekday name           #
            # %d → day number                  #
            # %B → full month name             #
            # %Y → full year                   #
            #                                  #
            # example:                         #
            # Monday, 11 May 2026              #
            # ---------------------------------#
            day_name = now.strftime("%A")
            day = now.strftime("%d")
            month = now.strftime("%B")
            year = now.strftime("%Y")
            sayAndWait(f"Today is {day_name}, {day} {month} {year}")

            command_matched = True

        # ----------------------------------#
        # fallback AI if AI mode is enabled #
        #                                   #
        # if no command matched,            #
        # AI handles the conversation       #
        # ----------------------------------#
        if not command_matched and ai_enabled:
            aiChat(query)

# Follow Me (Sameer Patra)

# GitHub   : https://github.com/Sam-Dev-161127
# LinkedIn : https://www.linkedin.com/in/sameer-patra-2b17a83a7
# X (Twitter) : https://x.com/Sam_Dev_161127
# Instagram : https://www.instagram.com/sam.dev.161127
# Telegram  : https://t.me/Sameer161127