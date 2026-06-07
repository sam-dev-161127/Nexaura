import speech_recognition as sr       # Converts microphone voice into text | pip install SpeechRecognition
import os                             # Used for file handling, opening apps, folders, songs, etc.
import glob                           # Finds files matching a pattern (like *.lnk, *.mp3)
import re                             # Used for pattern matching and cleaning text commands
import webbrowser                     # Opens websites directly in the default browser
import datetime                       # Gives current date, time, day, month, year, etc.
import config                         # Stores secret data like API keys separately
import random                         # Used for random replies, songs, jokes, choices, etc.
import threading                      # Runs multiple tasks at the same time (multitasking)
import win32com.client                # Windows built-in text to speech | pip install pywin32

# ------------------------------------------------------------
#   Nexaura - Your Personal Voice Assistant
#   main.py  |  Entry point
#
#   What this assistant can do:
#   ------------------------------------------------
#   - Listen to your voice and understand commands
#   - Open websites by saying "open youtube", "open google", etc.
#   - Launch desktop apps from a shortcut folder
#   - Chat with Google Gemini AI when AI mode is enabled
#   - Tell you the current time and date
#   - Stop speaking instantly when you say "stop"
#
#   How to get started:
#   ------------------------------------------------
#   1. Put your API key inside config.py like this:
#         API_KEY - "your-gemini-api-key-here"
#
#   2. Place your app shortcuts (.lnk files) inside the
#      folder path set in SHORTCUT_FOLDER below.
#      Example: telegram.lnk -> say "open telegram"
#
#   3. Run the script:
#         python main.py
#
#   Voice commands you can use:
#   ------------------------------------------------
#   "open youtube"      -> opens YouTube in browser
#   "open telegram"     -> launches telegram from shortcuts
#   "what time is it"   -> tells current time
#   "what date is it"   -> tells today\'s date
#   "enable ai"         -> switches to Gemini AI chat mode
#   "disable ai"        -> switches back to normal mode
#   "clear chat"        -> wipes AI conversation memory
#   "stop"              -> immediately stops Nexaura speaking
#
#   Technical notes for developers:
#   ------------------------------------------------
#   - TTS (text-to-speech) uses Windows SAPI via win32com.
#     This is Windows-only. For cross-platform, use pyttsx3.
#   - Speech recognition uses Google\'s free API (en-IN locale
#     works best for Indian accent and Hinglish words).
#   - Gemini is called via google.genai (new SDK).
#     Install it: pip install --upgrade google-genai
#   - App matching is case-insensitive substring matching.
#     You can improve it with fuzzy matching (fuzzywuzzy lib).
#
#   Author: Sameer Patra
#   GitHub : https://github.com/Sam-Dev-161127
# ------------------------------------------------------------


# ────────────────────────────────────────────────────────────
#   Text-to-Speech Engine Setup
#
#   We use Windows SAPI through win32com.
#   Think of `speaker` as Nexaura\'s voice box -
#   everything Nexaura says goes through this object.
#
#   speaker.Speak(text, flag) controls HOW it speaks:
#     flag - 0  ->  speak and wait (blocking)
#     flag - 1  ->  speak in background (non-blocking)
#     flag - 3  ->  cancel all speech immediately
# ────────────────────────────────────────────────────────────
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# True while Nexaura is currently talking
is_speaking = False

# Set this to True to make Nexaura shut up mid-sentence
stop_requested = False


# ────────────────────────────────────────────────────────────
#   Conversation Memory (Chat History)
#
#   This string stores the full back-and-forth conversation
#   between you and Nexaura. It gets sent to Gemini every
#   time so the AI knows the context of what was said before.
#
#   It looks like this inside:
#       Sam: what is python?
#       Nexaura: Python is a programming language...
#       Sam: who created it?
#       Nexaura: Guido van Rossum created Python...
#
#   Say "clear chat" to wipe this and start fresh.
# ────────────────────────────────────────────────────────────
chatStr = ""


# ────────────────────────────────────────────────────────────
#   AI Mode Toggle
#
#   False -> Normal mode  (Nexaura handles commands like
#                          opening apps, telling time, etc.)
#   True  -> AI mode      (Everything you say goes to Gemini)
#
#   Switch with voice:
#     "enable ai"   ->  turns AI mode ON
#     "disable ai"  ->  turns AI mode OFF
# ────────────────────────────────────────────────────────────
ai_enabled = False


# ────────────────────────────────────────────────────────────
#   Gemini AI Setup
#
#   We try to import the new google.genai SDK first.
#   If it\'s not installed, AI features will be disabled
#   and we\'ll print a message telling you what to install.
#
#   After import, we try to create:
#     - `client`  ->  the main Gemini API client object
#     - `model`   ->  only used as fallback for legacy SDK
#
#   The actual API call happens inside call_gemini() below.
# ────────────────────────────────────────────────────────────
try:
    import google.genai as genai
    NEW_GENAI = True
except Exception:
    # If google.genai isn\'t installed, disable AI completely.
    # Don\'t fall back to google.generativeai - it\'s deprecated
    # and throws FutureWarnings everywhere.
    genai = None
    NEW_GENAI = False
    print("-" * 60)
    print("  google.genai not installed - AI features disabled.")
    print("  To enable AI, run:")
    print("    pip install --upgrade google-genai")
    print("-" * 60)


# ────────────────────────────────────────────────────────────
#   Authenticate with the Gemini API
#
#   We support two styles depending on the SDK version:
#
#   New SDK  -> genai.Client(api_key - ...)
#              Use client.models.generate_content(...)
#
#   Old SDK  -> genai.configure(api_key - ...)
#              Use genai.GenerativeModel(...).generate_content(...)
#
#   We always prefer the new SDK. The old one is kept only
#   as a silent fallback so nothing breaks unexpectedly.
# ────────────────────────────────────────────────────────────
client = None   # new SDK client object
model  = None   # legacy SDK model object (fallback only)

if genai is not None:

    # Try new SDK: create a Client object
    if hasattr(genai, "Client"):
        try:
            client = genai.Client(api_key=config.API_KEY)
            print("Gemini: client created (new SDK)")
        except Exception as e:
            print("Gemini client error:", e)
            client = None

    # Try old SDK: configure + create GenerativeModel
    if client is None and hasattr(genai, "configure"):
        try:
            genai.configure(api_key=config.API_KEY)
            if hasattr(genai, "GenerativeModel"):
                model = genai.GenerativeModel("gemini-2.5-flash")
                print("Gemini: model created (legacy SDK fallback)")
        except Exception as e:
            print("Gemini legacy setup error:", e)
            model = None


# ────────────────────────────────────────────────────────────
#   Gemini API: Print which backend is active
#
#   This runs once at startup so you know what\'s working.
#   If you see "none available" it means something went wrong
#   during the import or auth steps above.
# ────────────────────────────────────────────────────────────
try:
    if genai is not None:
        backend = "google.genai (new)" if NEW_GENAI else "google.generativeai (legacy)"
        available_attrs = [
            attr for attr in
            ("configure", "Client", "Model", "GenerativeModel", "generate_text")
            if hasattr(genai, attr)
        ]
        print(f"Gemini backend : {backend}")
        print(f"Available APIs : {', '.join(available_attrs) if available_attrs else 'none'}")
        print(f"Client ready   : {'yes' if client is not None else 'no'}")
        print(f"Model  ready   : {'yes' if model  is not None else 'no'}")
except Exception as e:
    print("Gemini diagnostic error:", e)


# ────────────────────────────────────────────────────────────
#   call_gemini(prompt)
#
#   This is the ONLY place where we talk to the Gemini API.
#   Pass in the full conversation string (chatStr) and it
#   returns Gemini\'s reply as plain text.
#
#   It tries two paths in order:
#     1. New SDK  -> client.models.generate_content(...)
#     2. Old SDK  -> model.generate_content(...)  (fallback)
#
#   Returns "" if both fail, so the rest of the code doesn\'t
#   crash - it just handles the empty string gracefully.
#
#   WHY THIS FUNCTION EXISTS:
#   --------------------------
#   The old code used a GenAICompat wrapper class that was
#   accidentally calling itself in a loop, so generate_content
#   always returned "" silently. That\'s why questions like
#   "what is python" never got a response. This function
#   replaces that broken wrapper with a clean, direct call.
# ────────────────────────────────────────────────────────────
def call_gemini(prompt):

    # Path 1: New google.genai SDK
    # Uses client.models.generate_content() - the correct
    # way to call Gemini in the new SDK (2024+)
    if client is not None and hasattr(client, "models"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("Gemini new SDK error:", e)

    # Path 2: Legacy google.generativeai SDK fallback
    # Uses the older GenerativeModel().generate_content()
    if model is not None and hasattr(model, "generate_content"):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("Gemini legacy SDK error:", e)

    # If both failed, tell the developer and return empty
    print("Gemini: no working backend found - check your API key and SDK install")
    return ""


# ────────────────────────────────────────────────────────────
#   clean_for_speech(text)
#
#   AI responses often come back with markdown formatting:
#   **bold**, # headings, `code blocks`, [links](url), etc.
#   That looks fine in a chat UI but sounds terrible when
#   spoken out loud - "hashtag hashtag Introduction" is awful.
#
#   This function strips all of that and returns clean,
#   natural-sounding text suitable for TTS.
#
#   What it removes:
#     **bold** / *italic*  ->  just the text inside
#     ## Headings          ->  removed entirely
#     `code` blocks        ->  removed entirely
#     [link text](url)     ->  keeps only "link text"
#     - bullet points      ->  removed
#     multiple newlines    ->  replaced with single space
#     double spaces        ->  collapsed to one
# ────────────────────────────────────────────────────────────
def clean_for_speech(text):

    # Remove bold (**text**) and italic (*text*) markdown
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)

    # Remove markdown headings (# Title, ## Subtitle, etc.)
    text = re.sub(r'#{1,6}\s*', '', text)

    # Remove inline code (`code`) and code blocks (```code```)
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)

    # Remove markdown links but keep the visible text
    # Example: [Google](https://google.com) -> "Google"
    # We do this manually instead of regex to avoid edge cases
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
            out_parts.append(s[i:start])          # text before [
            out_parts.append(s[start + 1:mid])    # visible link text
            i = end + 1
        out_parts.append(s[i:])
        return ''.join(out_parts)

    text = _strip_md_links(text)

    # Remove bullet point markers at the start of lines
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)

    # Replace line breaks with a single space (flatten to one line)
    text = re.sub(r'\n+', ' ', text)

    # Collapse multiple spaces into one
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


# ────────────────────────────────────────────────────────────
#   sayAndWait(text)  -  Speak and BLOCK until done
#
#   Use this when you need Nexaura to FINISH talking before
#   doing something else - like opening a browser or an app.
#   If you don\'t wait, the app launches while Nexaura is still
#   mid-sentence, which feels broken.
#
#   It also splits long text into individual sentences before
#   speaking. This does two things:
#     1. Makes speech smoother and more natural
#     2. Allows "stop" to interrupt between sentences quickly
#        instead of waiting for a huge chunk to finish
#
#   The `stop_requested` flag is checked before each sentence
#   so Nexaura can shut up almost instantly when you say "stop".
# ────────────────────────────────────────────────────────────
def sayAndWait(text):
    global is_speaking
    global stop_requested

    # Clean markdown before speaking
    text = clean_for_speech(text)

    # Don\'t even start if a stop was already requested
    if stop_requested:
        return

    print("Nexaura :", text)
    is_speaking = True

    # Split on sentence-ending punctuation followed by a space
    # so each sentence is spoken one at a time
    sentences = re.split(r'(?<=[.!?]) +', text)

    for sentence in sentences:

        # Check between sentences - stop immediately if requested
        if stop_requested:
            # SVSFPurgeBeforeSpeak flag (3):
            # clears the current speech AND the queue instantly
            speaker.Speak("", 3)
            break

        # flag 0 - speak and wait (blocking)
        speaker.Speak(sentence, 0)

    # Reset flags once done
    is_speaking = False
    stop_requested = False


# ────────────────────────────────────────────────────────────
#   say(text)  -  Speak in the BACKGROUND (non-blocking)
#
#   Use this for long AI replies where you don\'t want the
#   program to freeze while Nexaura is talking. It spins up
#   a background thread that calls sayAndWait internally.
#
#   The thread is marked as daemon - True so it auto-closes
#   when the main program exits (no zombie threads).
# ────────────────────────────────────────────────────────────
def say(text):
    threading.Thread(target=sayAndWait, args=(text,), daemon=True).start()


# ────────────────────────────────────────────────────────────
#   stopSpeaking()  -  Shut Nexaura up immediately
#
#   Sets the stop flag AND purges the SAPI speech queue so
#   Nexaura goes silent within milliseconds. Called when
#   the user says "stop" during any speech.
#
#   The SVSFPurgeBeforeSpeak flag (3) tells SAPI to:
#     - Drop the word it\'s currently speaking
#     - Clear everything waiting in the queue
#   Result: instant silence.
# ────────────────────────────────────────────────────────────
def stopSpeaking():
    global is_speaking
    global stop_requested

    try:
        stop_requested = True
        is_speaking = False

        # Flag 3 - SVSFPurgeBeforeSpeak - kills speech instantly
        speaker.Speak("", 3)

        print("Nexaura stopped speaking")

    except Exception as e:
        print("Stop error:", e)


# ────────────────────────────────────────────────────────────
#   clearChat()  -  Wipe the AI conversation memory
#
#   Resets chatStr to empty so Gemini starts fresh with no
#   previous context. Useful when:
#     - The conversation went off-track
#     - You want to ask about a completely different topic
#     - Gemini is confused because of old context
#
#   Voice command: "clear chat"
# ────────────────────────────────────────────────────────────
def clearChat():
    global chatStr

    chatStr = ""
    sayAndWait("Chat cleared")


# ────────────────────────────────────────────────────────────
#   aiChat(query)  -  Send your question to Gemini and reply
#
#   This is the core AI function. Here\'s exactly what happens:
#
#     1. Your question gets added to chatStr
#        (so Gemini has full context of the conversation)
#
#     2. chatStr is sent to Gemini via call_gemini()
#        (the whole conversation, not just this one question)
#
#     3. Gemini\'s reply gets added to chatStr too
#        (so future questions can reference this answer)
#
#     4. The reply is printed and spoken aloud
#
#     5. A text file with the reply is saved to the Gemini/ folder
#        (named after your question, so it\'s easy to find later)
#
#   NOTE: The full chat history is printed to the terminal
#   after every exchange so you can follow the conversation.
# ────────────────────────────────────────────────────────────
def aiChat(query):
    global chatStr
    global stop_requested

    # Always reset stop flag before a new AI reply starts
    stop_requested = False

    # Add user\'s message to conversation history
    chatStr += f"Sam: {query}\nNexaura: "

    # Send the full conversation to Gemini and get a reply
    reply = call_gemini(chatStr)

    # Handle the case where Gemini returned nothing
    if not reply:
        sayAndWait("Sorry Sam, I could not get a response. Please check your API key or internet connection.")
        return

    # Add Gemini\'s reply to the conversation history
    chatStr += f"{reply}\n"

    # ── Print full chat history to terminal ──────────────────
    # This lets you see the whole conversation so far,
    # which is useful for debugging and following along.
    print("\n" + "-" * 50)
    print("  Chat History")
    print("-" * 50)
    print(chatStr.strip())
    print("-" * 50 + "\n")

    # Speak the reply in the background so the program doesn\'t freeze
    say(reply)

    # ── Save reply to a text file ─────────────────────────────
    # Creates a Gemini/ folder if it doesn\'t exist yet.
    # Each conversation is saved as a .txt file named after
    # the query - handy for reviewing past AI answers.
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # Clean up the query to use as a filename
    filename = query.replace("using artificial intelligence", "").strip()

    # Windows doesn\'t allow these characters in filenames:
    # \ / : * ? " < > |   <- strip them all out
    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    # If the query was empty or got fully stripped, use a random name
    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    # Save the AI reply (not the full chatStr) to the file
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# ────────────────────────────────────────────────────────────
#   useAI(query)  -  Handle AI-related voice commands
#
#   This runs BEFORE any other command processing.
#   It intercepts AI control commands ("stop", "enable ai",
#   "disable ai", "clear chat") and routes everything else
#   to aiChat() if AI mode is currently on.
#
#   Returns True  ->  command was handled (skip further checks)
#   Returns False ->  not an AI command (keep checking below)
#
#   "stop" is always checked FIRST so it works even while
#   Nexaura is mid-sentence during an AI reply.
# ────────────────────────────────────────────────────────────
def useAI(query):
    global ai_enabled

    # ── "stop" should ALWAYS work, even inside AI mode ───────
    # Check this before anything else so it can\'t be blocked
    if "stop" in query:
        stopSpeaking()
        return True

    # Turn ON Gemini AI conversation mode
    if "enable ai" in query:
        ai_enabled = True
        sayAndWait("AI enabled")
        return True

    # Turn OFF Gemini AI conversation mode
    if "disable ai" in query:
        ai_enabled = False
        sayAndWait("AI disabled")
        return True

    # Wipe the conversation memory and start fresh
    if "clear chat" in query:
        clearChat()
        return True

    # If AI mode is on, send any unrecognised command to Gemini
    if ai_enabled:
        aiChat(query)
        return True

    # Not an AI-related command - let the normal handler deal with it
    return False


# ────────────────────────────────────────────────────────────
#   get_mic_index()  -  Find the right microphone to use
#
#   Scans all connected audio input devices and returns
#   the index of the best microphone found.
#
#   Priority order:
#     1. Realtek microphone (common on laptops/desktops)
#     2. Any device with "microphone" in the name
#     3. None - if nothing is found
#
#   The index is then passed to sr.Microphone(device_index - ...)
#   so we use the correct mic and not some random audio input.
# ────────────────────────────────────────────────────────────
def get_mic_index():

    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):

        mic_name = name.lower()

        # ── Realtek detection ─────────────────────────────────
        # Works for: Realtek HD Audio, Realtek(R) Audio,
        # Microphone Array (Realtek), laptop built-in mics, etc.
        if "realtek" in mic_name:
            return i

        # ── Generic fallback ──────────────────────────────────
        # Catches most USB mics, headset mics, and anything
        # whose name simply contains the word "microphone"
        if "microphone" in mic_name:
            return i

    # No suitable microphone found - will be handled in takeCommand()
    return None


# ────────────────────────────────────────────────────────────
#   takeCommand()  -  Listen and convert speech to text
#
#   Opens the microphone, listens for your voice, and returns
#   the recognized text in lowercase. Returns "" on failure.
#
#   What each setting does:
#   ------------------------------------------------
#   energy_threshold        -> mic sensitivity (lower - picks
#                             up quieter sounds; 200 is good
#                             for most quiet rooms)
#
#   dynamic_energy_threshold -> True - auto-adjusts threshold
#                              based on ambient noise levels
#
#   pause_threshold          -> seconds of silence after you stop
#                              speaking before it stops listening
#                              (1.2s gives a natural pause)
#
#   adjust_for_ambient_noise -> calibrates to room noise before
#                              listening (2s recommended for
#                              Indian environments with fans/AC)
#
#   timeout                  -> max seconds to wait for you to
#                              START speaking (5s then gives up)
#
#   phrase_time_limit        -> max seconds to listen once you\'ve
#                              started speaking (7s is enough
#                              for most commands)
#
#   language - 'en-IN'       -> Indian English - gives best results
#                              for Indian accents, Hinglish words,
#                              and Indian names/pronunciations
# ────────────────────────────────────────────────────────────
def takeCommand():

    r = sr.Recognizer()

    # Mic sensitivity and timing settings
    r.energy_threshold        = 200
    r.dynamic_energy_threshold = True
    r.pause_threshold         = 1.2

    mic_index = get_mic_index()

    # If no mic is found, skip this loop iteration
    if mic_index is None:
        print("No microphone found - check your audio input devices")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            # Calibrate to background noise before listening
            # Increase to 2.0+ if you\'re in a noisy environment
            r.adjust_for_ambient_noise(source, duration=2)

            print("Listening...")

            # Wait up to 5s for you to start speaking,
            # then record up to 7s of your voice
            audio = r.listen(source, timeout=5, phrase_time_limit=7)

            print("Recognizing...")

            # Use Google Speech Recognition with Indian English
            query = r.recognize_google(audio, language='en-IN')

            print("You said:", query)

            return query.lower()

    except sr.WaitTimeoutError:
        # You didn\'t start speaking within 5 seconds - that\'s fine, just loop
        print("Listening timeout - no speech detected")
        return ""

    except sr.UnknownValueError:
        # Could hear something but couldn\'t understand it
        print("Could not understand audio")
        sayAndWait("Sorry Sam, I could not understand. Could you say that again?")
        return ""

    except Exception as e:
        # Microphone device error or some other unexpected issue
        print("Microphone error:", e)
        return ""


# ------------------------------------------------------------
#   MAIN PROGRAM - Everything below runs when you start Nexaura
# ------------------------------------------------------------

if __name__ == '__main__':

    print("-" * 50)
    print("  Nexaura started - listening for your voice")
    print("-" * 50)

    sayAndWait("I am Nexaura AI")

    # ────────────────────────────────────────────────────────
    #   Websites List
    #
    #   Add websites here that you want to open by voice.
    #   Format: ["spoken name", "full URL"]
    #
    #   Example: saying "open youtube" opens youtube.com
    #
    #   To add a new site, just copy any line and change
    #   the name and URL. Keep names short and easy to say.
    # ────────────────────────────────────────────────────────
    sites = [
        ["youtube",         "https://www.youtube.com"],
        ["google",          "https://www.google.com"],
        ["wikipedia",       "https://www.wikipedia.org"],
        ["gmail",           "https://mail.google.com"],
        ["twitter",         "https://www.x.com"],
        ["linkedin",        "https://www.linkedin.com"],
        ["amazon",          "https://www.amazon.in"],
        ["flipkart",        "https://www.flipkart.com"],
        ["netflix",         "https://www.netflix.com"],
        ["spotify",         "https://www.spotify.com"],
        ["jiohotstar",      "https://www.jiohotstar.com"],
        ["code with harry", "https://www.codewithharry.com"],
        ["geeksforgeeks",   "https://www.geeksforgeeks.org"],
        ["w3schools",       "https://www.w3schools.com"],
        ["leetcode",        "https://leetcode.com"],
        ["hackerrank",      "https://www.hackerrank.com"],
        ["stackoverflow",   "https://stackoverflow.com"],
        ["canva",           "https://www.canva.com"],
        ["replit",          "https://replit.com"],
        ["coursera",        "https://www.coursera.org"],
    ]


    # ────────────────────────────────────────────────────────
    #   Shortcut Folder - Launch Desktop Apps by Voice
    #
    #   Place .lnk (shortcut) or .mp3 files in this folder.
    #   Nexaura scans them at startup and builds a dictionary
    #   mapping the filename -> full path.
    #
    #   How it works:
    #     - telegram.lnk  -> say "open telegram"
    #     - vscode.lnk    -> say "open vscode"
    #     - believer.mp3  -> say "play believer"
    #
    #   Change SHORTCUT_FOLDER to your own folder path.
    #   Make sure the folder exists or you\'ll get no apps loaded.
    # ────────────────────────────────────────────────────────
    SHORTCUT_FOLDER = r"C:\Users\Sam-Dev-161127\PycharmProjects\Nexaura\Shortcut"

    # This dictionary maps spoken name -> full file path
    # It gets populated by the scanner below
    apps = {}

    # ── Scan .lnk shortcut files ──────────────────────────────
    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.lnk")):
        # Strip the .lnk extension and normalize to lowercase
        # so "Telegram.lnk" and "telegram.lnk" both match "telegram"
        app_name = os.path.basename(shortcut).replace(".lnk", "").lower().strip()
        apps[app_name] = shortcut

    # ── Scan .mp3 files (songs, audio) ───────────────────────
    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.mp3")):
        app_name = os.path.basename(shortcut).replace(".mp3", "").lower().strip()
        apps[app_name] = shortcut

    # Print how many apps were loaded so you can verify the folder scan worked
    print(f"Loaded {len(apps)} shortcut(s) from: {SHORTCUT_FOLDER}")


    # ────────────────────────────────────────────────────────
    #   clean_command(command)
    #
    #   Before matching a voice command to an app name, we
    #   strip out filler words like "open", "start", "play".
    #   This way "open telegram" and "launch telegram" both
    #   resolve to just "telegram" for matching.
    # ────────────────────────────────────────────────────────
    def clean_command(command):

        # Words to strip out before matching against app names
        remove_words = ["open", "start", "launch", "play", "please"]

        command = command.lower()

        for word in remove_words:
            command = command.replace(word, "")

        return command.strip()


    # ────────────────────────────────────────────────────────
    #   open_app(command)
    #
    #   Tries to match the voice command to a shortcut in the
    #   `apps` dictionary and launches it using os.startfile().
    #
    #   Two matching strategies:
    #     1. Exact match   -> "telegram" matches "telegram"
    #     2. Partial match -> "believer" matches "believer imagine dragons"
    #                        "play imagine" also matches it
    #
    #   Returns True if an app was launched, False if not found.
    # ────────────────────────────────────────────────────────
    def open_app(command):

        command_clean = clean_command(command)

        print("Cleaned command:", command_clean)

        # ── Strategy 1: Exact match ───────────────────────────
        if command_clean in apps:
            sayAndWait("Opening " + command_clean)
            os.startfile(apps[command_clean])
            return True

        # ── Strategy 2: Partial / substring match ─────────────
        # Check if what you said is inside an app name
        # OR if an app name is inside what you said
        # This handles cases like "play believer imagine dragons"
        for name in apps:
            if command_clean in name or name in command_clean:
                sayAndWait("Opening " + name)
                os.startfile(apps[name])
                return True

        # Nothing matched
        return False


    # ------------------------------------------------------------
    #   MAIN LOOP - Nexaura listens forever until you close it
    #
    #   Every iteration:
    #     1. Listen for a voice command
    #     2. Check AI commands first (stop, enable/disable, etc.)
    #     3. Try to open an app from the shortcuts folder
    #     4. Try to open a website from the sites list
    #     5. Tell time or date if asked
    #     6. If AI mode is on and nothing matched -> send to Gemini
    # ------------------------------------------------------------
    while True:

        query = takeCommand()

        # Nothing was heard - just keep listening
        if query == "":
            continue

        # Track whether any command was successfully matched
        command_matched = False

        # ── Step 1: AI commands (always check these first) ────
        # "stop", "enable ai", "disable ai", "clear chat",
        # and anything said while AI mode is on
        if useAI(query):
            continue

        # ── Step 2: Try opening an app from shortcuts ──────────
        if open_app(query):
            continue

        # ── Step 3: Open websites ──────────────────────────────
        # sayAndWait so Nexaura finishes speaking BEFORE the
        # browser opens (otherwise it feels glitchy)
        for site in sites:
            if f"open {site[0]}" in query:
                sayAndWait("Opening " + site[0])
                webbrowser.open(site[1])
                command_matched = True
                break  # stop after first website match

        # ── Step 4: Check for open/launch keywords again ───────
        # This catches cases where open_app() was skipped above
        # but the user said "open X" or "launch X"
        if any(kw in query for kw in ("open ", "start ", "launch ", "play")):
            if open_app(query):
                command_matched = True

        # ── Step 5: Tell the current time ──────────────────────
        if "what time is it" in query:
            now = datetime.datetime.now()

            # 12-hour format with AM/PM
            # %I - hour (12-hour), %M - minutes, %p - AM/PM
            hour   = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm  = now.strftime("%p")

            sayAndWait(f"The time is {hour}:{minute} {am_pm}")
            command_matched = True

        # ── Step 6: Tell today\'s date ──────────────────────────
        if "what date is it" in query:
            now = datetime.datetime.now()

            # Full human-readable date: "Monday, 11 May 2026"
            # %A - full weekday, %d - day, %B - full month, %Y - year
            day_name = now.strftime("%A")
            day      = now.strftime("%d")
            month    = now.strftime("%B")
            year     = now.strftime("%Y")

            sayAndWait(f"Today is {day_name}, {day} {month} {year}")
            command_matched = True

        # ── Step 7: AI fallback ────────────────────────────────
        # If AI mode is on and none of the above commands matched,
        # assume the user is talking to Gemini and forward it
        if not command_matched and ai_enabled:
            aiChat(query)

# -------------------------------------------------------------------#
#   About the Developer                                              #
#                                                                    #
#   👋 Hi, I'm Sameer Patra.                                         #
#                                                                    #
#   🚀 Python Developer & AI Enthusiast                              #
#   🤖 Creator of Nexaura                                            #
#   🎮 Aspiring Game Developer                                       #
#   🐧 Linux (Ubuntu) User                                           #
#   💻 Learning C, HTML, CSS, and Advanced Python                    #
#   🔬 Interested in Robotics, AI, and Automation                    #
#                                                                    #
#   🏆 Certifications                                                #
#   • Google Certified Python Developer                              #
#     Certificate Verification:                                      #
#     https://coursera.org/verify/IKPW8JE4BPJP                       #
#                                                                    #
#   I enjoy building AI assistants, automation tools,                #
#   robotics projects, and innovative software that                  #
#   combines technology with real-world applications.                #
# -------------------------------------------------------------------#
#                                                                    #
#   Follow Me (Sameer Patra)                                         #
#                                                                    #
#   GitHub      : https://github.com/Sam-Dev-161127                  #
#   LinkedIn    : https://www.linkedin.com/in/sameer-patra-2b17a83a7 #
#   X (Twitter) : https://x.com/Sam_Dev_161127                       #
#   Instagram   : https://www.instagram.com/sam.dev.161127           #
#   Telegram    : https://t.me/Sameer161127                          #
#   Email       : sam.dev1611@gmail.com                              #
# -------------------------------------------------------------------#
