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
from collections import namedtuple   # For creating Website data structure

# ------------------------------------------------------------
#   Nexaura - Voice Assistant
#   Author: Sameer Patra | GitHub: https://github.com/Sam-Dev-161127
# ------------------------------------------------------------


# ────────────────────────────────────────────────────────────
#   Global Constants
# ────────────────────────────────────────────────────────────
MIC_ENERGY_THRESHOLD = 200
MIC_AMBIENT_DURATION = 2
MIC_LISTEN_TIMEOUT = 5
MIC_PHRASE_TIME_LIMIT = 7
MIC_PAUSE_THRESHOLD = 1.2

SPEECH_FLAG_WAIT = 0
SPEECH_FLAG_BACKGROUND = 1
SPEECH_FLAG_PURGE = 3

SENTENCE_SPLITTER = r'(?<=[.!?]) +'
FILENAME_INVALID_CHARS = r'[\\/:*?"<>|]'

Website = namedtuple('Website', ['name', 'url'])
SHORTCUT_FOLDER = r"C:\Users\Sam-Dev-161127\PycharmProjects\Nexaura\Shortcut"


# ────────────────────────────────────────────────────────────
#   Text-to-Speech Engine
# ────────────────────────────────────────────────────────────
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# True while Nexaura is currently talking
is_speaking = False

# Set this to True to make Nexaura shut up mid-sentence
stop_requested = False


# Conversation history
chatStr = ""

# AI mode toggle
ai_enabled = False


# ────────────────────────────────────────────────────────────
#   Gemini AI Setup
# ────────────────────────────────────────────────────────────
try:
    import google.genai as genai
    NEW_GENAI = True
except Exception:
    genai = None
    NEW_GENAI = False
    print("-" * 60)
    print("  google.genai not installed - AI features disabled.")
    print("  To enable AI, run:")
    print("    pip install --upgrade google-genai")
    print("-" * 60)


# Authenticate with Gemini API - try new SDK first, fallback to legacy
client = None
model  = None

if genai is not None:

    if hasattr(genai, "Client"):
        try:
            client = genai.Client(api_key=config.API_KEY)
            print("Gemini: client created (new SDK)")
        except Exception as e:
            print("Gemini client error:", e)
            client = None

    if client is None and hasattr(genai, "configure"):
        try:
            genai.configure(api_key=config.API_KEY)
            if hasattr(genai, "GenerativeModel"):
                model = genai.GenerativeModel("gemini-2.5-flash")
                print("Gemini: model created (legacy SDK fallback)")
        except Exception as e:
            print("Gemini legacy setup error:", e)
            model = None


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


# Send prompt to Gemini API (new SDK first, legacy fallback)
def call_gemini(prompt):

    if client is not None and hasattr(client, "models"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("Gemini new SDK error:", e)

    if model is not None and hasattr(model, "generate_content"):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("Gemini legacy SDK error:", e)

    print("Gemini: no working backend found - check your API key and SDK install")
    return ""


# Remove markdown formatting from text for natural speech output
def clean_for_speech(text):

    # Remove bold and italic markdown
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)

    # Remove markdown links but keep visible text: [text](url) -> text
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
            out_parts.append(s[i:start])
            out_parts.append(s[start + 1:mid])
            i = end + 1
        out_parts.append(s[i:])
        return ''.join(out_parts)

    text = _strip_md_links(text)

    # Remove bullet points, flatten newlines, collapse spaces
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


# Speak text and wait for completion (blocks until done)
def sayAndWait(text):
    global is_speaking
    global stop_requested

    text = clean_for_speech(text)

    if stop_requested:
        return

    print("Nexaura :", text)
    is_speaking = True

    sentences = re.split(SENTENCE_SPLITTER, text)

    for sentence in sentences:
        if stop_requested:
            speaker.Speak("", SPEECH_FLAG_PURGE)
            break
        speaker.Speak(sentence, SPEECH_FLAG_WAIT)

    is_speaking = False
    stop_requested = False


# Speak text in background (non-blocking)
def say(text):
    threading.Thread(target=sayAndWait, args=(text,), daemon=True).start()


# Stop speaking immediately
def stopSpeaking():
    global is_speaking
    global stop_requested

    try:
        stop_requested = True
        is_speaking = False
        speaker.Speak("", SPEECH_FLAG_PURGE)
        print("Nexaura stopped speaking")

    except Exception as e:
        print("Stop error:", e)


# Clear conversation history
def clearChat():
    global chatStr

    chatStr = ""
    sayAndWait("Chat cleared")


# Send query to Gemini and speak/save the response
def aiChat(query):
    global chatStr
    global stop_requested

    stop_requested = False
    chatStr += f"Sam: {query}\nNexaura: "
    reply = call_gemini(chatStr)

    if not reply:
        sayAndWait("Sorry Sam, I could not get a response. Please check your API key or internet connection.")
        return

    chatStr += f"{reply}\n"

    print("\n" + "-" * 50)
    print("  Chat History")
    print("-" * 50)
    print(chatStr.strip())
    print("-" * 50 + "\n")

    say(reply)

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    filename = query.replace("using artificial intelligence", "").strip()
    filename = re.sub(FILENAME_INVALID_CHARS, '', filename).strip()

    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# Handle AI-related voice commands
def useAI(query):
    global ai_enabled

    if "stop" in query:
        stopSpeaking()
        return True

    if "enable ai" in query:
        ai_enabled = True
        sayAndWait("AI enabled")
        return True

    if "disable ai" in query:
        ai_enabled = False
        sayAndWait("AI disabled")
        return True

    if "clear chat" in query:
        clearChat()
        return True

    if ai_enabled:
        aiChat(query)
        return True

    return False


# Find the best microphone to use
def get_mic_index():

    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):
        mic_name = name.lower()

        if "realtek" in mic_name:
            return i

        if "microphone" in mic_name:
            return i

    return None


# Listen for voice input and return recognized text
def takeCommand():

    r = sr.Recognizer()

    r.energy_threshold        = MIC_ENERGY_THRESHOLD
    r.dynamic_energy_threshold = True
    r.pause_threshold         = MIC_PAUSE_THRESHOLD

    mic_index = get_mic_index()

    if mic_index is None:
        print("No microphone found - check your audio input devices")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            r.adjust_for_ambient_noise(source, duration=MIC_AMBIENT_DURATION)

            print("Listening...")

            audio = r.listen(source, timeout=MIC_LISTEN_TIMEOUT, phrase_time_limit=MIC_PHRASE_TIME_LIMIT)

            print("Recognizing...")

            query = r.recognize_google(audio, language='en-IN')

            print("You said:", query)

            return query.lower()

    except sr.WaitTimeoutError:
        print("Listening timeout - no speech detected")
        return ""

    except sr.UnknownValueError:
        print("Could not understand audio")
        sayAndWait("Sorry Sam, I could not understand. Could you say that again?")
        return ""

    except Exception as e:
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

    # Websites list
    sites = [
        Website("youtube",         "https://www.youtube.com"),
        Website("google",          "https://www.google.com"),
        Website("wikipedia",       "https://www.wikipedia.org"),
        Website("gmail",           "https://mail.google.com"),
        Website("twitter",         "https://www.x.com"),
        Website("linkedin",        "https://www.linkedin.com"),
        Website("amazon",          "https://www.amazon.in"),
        Website("flipkart",        "https://www.flipkart.com"),
        Website("netflix",         "https://www.netflix.com"),
        Website("spotify",         "https://www.spotify.com"),
        Website("jiohotstar",      "https://www.jiohotstar.com"),
        Website("code with harry", "https://www.codewithharry.com"),
        Website("geeksforgeeks",   "https://www.geeksforgeeks.org"),
        Website("w3schools",       "https://www.w3schools.com"),
        Website("leetcode",        "https://leetcode.com"),
        Website("hackerrank",      "https://www.hackerrank.com"),
        Website("stackoverflow",   "https://stackoverflow.com"),
        Website("canva",           "https://www.canva.com"),
        Website("replit",          "https://replit.com"),
        Website("coursera",        "https://www.coursera.org"),
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
    #   Change SHORTCUT_FOLDER constant (at the top) to your own folder path.
    #   Make sure the folder exists or you\'ll get no apps loaded.
    # ────────────────────────────────────────────────────────

    # This dictionary maps spoken name -> full file path
    # It gets populated by the scanner below
    apps = {}

    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.lnk")):
        app_name = os.path.basename(shortcut).replace(".lnk", "").lower().strip()
        apps[app_name] = shortcut

    for shortcut in glob.glob(os.path.join(SHORTCUT_FOLDER, "*.mp3")):
        app_name = os.path.basename(shortcut).replace(".mp3", "").lower().strip()
        apps[app_name] = shortcut

    print(f"Loaded {len(apps)} shortcut(s) from: {SHORTCUT_FOLDER}")

    # Strip filler words from command before matching
    def clean_command(command):
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

        if command_clean in apps:
            sayAndWait("Opening " + command_clean)
            os.startfile(apps[command_clean])
            return True

        for name in apps:
            if command_clean in name or name in command_clean:
                sayAndWait("Opening " + name)
                os.startfile(apps[name])
                return True

        return False


    # Main loop
    while True:

        query = takeCommand()

        if query == "":
            continue

        command_matched = False

        # Check AI commands first
        if useAI(query):
            continue

        # Try opening apps
        if open_app(query):
            continue

        # Open websites
        for site in sites:
            if f"open {site.name}" in query:
                sayAndWait("Opening " + site.name)
                webbrowser.open(site.url)
                command_matched = True
                break

        # Check for open/launch keywords
        if any(kw in query for kw in ("open ", "start ", "launch ", "play")):
            if open_app(query):
                command_matched = True

        # Tell current time
        if "what time is it" in query:
            now = datetime.datetime.now()
            hour   = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm  = now.strftime("%p")
            sayAndWait(f"The time is {hour}:{minute} {am_pm}")
            command_matched = True

        # Tell current date
        if "what date is it" in query:
            now = datetime.datetime.now()
            day_name = now.strftime("%A")
            day      = now.strftime("%d")
            month    = now.strftime("%B")
            year     = now.strftime("%Y")
            sayAndWait(f"Today is {day_name}, {day} {month} {year}")
            command_matched = True

        # Send to Gemini if AI mode is on
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
