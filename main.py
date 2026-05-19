import speech_recognition as sr       # Converts microphone voice into text | pip install SpeechRecognition
import os                             # Used for file handling, opening apps, folders, songs, etc.
import re                             # Used for pattern matching and cleaning text commands
import webbrowser                     # Opens websites directly in the default browser
import datetime                       # Gives current date, time, day, month, year, etc.
import google.generativeai as genai   # Gemini AI integration for AI chat features | pip install google-generativeai
import config                         # Stores secret data like API keys separately
import random                         # Used for random replies, songs, jokes, choices, etc.
import threading                      # Runs multiple tasks at the same time (multitasking)
import time                           # Used for adding delay between tasks
import win32com.client                # Windows built-in text to speech | pip install pywin32


# Windows built-in speaker — much more reliable than pyttsx3 on Windows
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# flag to cancel speaking mid-sentence
is_speaking = False

# flag to stop current AI speech instantly
stop_requested = False

# store chat history
# stores previous conversation between user and Nexaura
# helps AI remember conversation context
#
# example:
# Sam: hello
# Nexaura: hi
chatStr = ""

# AI mode toggle
# Primary Mode  -> AI Enabled  (Gemini AI conversation mode)
# Secondary Mode -> AI Disabled (Normal command execution mode)
# False → normal assistant mode
# True  → AI conversation mode
# voice commands:
# "enable ai"
# "disable ai"
ai_enabled = False

# configure Gemini API using your key
# API key is stored separately for security reasons
# NEVER share your API key publicly
genai.configure(api_key=config.API_KEY)

# create Gemini model
# flash → faster responses
# pro   → smarter but slower
# flash is recommended for nexaura assistants
model = genai.GenerativeModel("gemini-2.5-flash")


# clean AI response so voice sounds natural
def clean_for_speech(text):

    # remove bold and italic markdown
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)

    # remove markdown headings
    text = re.sub(r'#{1,6}\s*', '', text)

    # remove inline and multiline code blocks
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)

    # remove markdown links but keep visible text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # remove bullet points
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)

    # replace multiple lines with single space
    text = re.sub(r'\n+', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


# speak and WAIT until fully done before doing next action
# always use this before opening apps, songs, games, websites
def sayAndWait(text):
    global is_speaking
    global stop_requested

    text = clean_for_speech(text)

    # do not speak if stop was requested
    if stop_requested:
        return

    print("Nexaura :", text)
    is_speaking = True

    # split long AI response into smaller chunks
    # helps:
    # - smoother speech playback
    # - faster stop response
    # - prevents long speech freezing
    sentences = re.split(r'(?<=[.!?]) +', text)

    for sentence in sentences:

        # instantly stop if user says stop
        if stop_requested:

            # SVSFPurgeBeforeSpeak flag = 3
            # clears:
            # - current speech
            # - queued speech
            # allows instant interruption
            speaker.Speak("", 3)
            break

        speaker.Speak(sentence, 0)

    is_speaking = False
    stop_requested = False


# speak without waiting — used only for long AI replies
# daemon=True means thread automatically closes
# when main program exits
def say(text):
    threading.Thread(target=sayAndWait, args=(text,), daemon=True).start()


# stop speaking immediately — works even during AI long replies
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


# clear chat memory
# removes stored AI conversation history
# useful if AI starts giving confusing replies
def clearChat():
    global chatStr

    chatStr = ""
    sayAndWait("Chat cleared")


# AI chat function using Gemini
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

    # create Gemini folder if not present
    # this folder stores all AI conversation logs as text files
    # you can rename:
    # "Gemini"
    # "Chats"
    # "AI Logs"
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # remove unwanted text from filename
    filename = query.replace("using artificial intelligence", "").strip()

    # remove invalid Windows filename characters
    # Windows does NOT allow:
    # \ / : * ? " < > |
    # without cleanup:
    # file saving may fail
    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    # create random filename if query is empty
    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    # save AI response into text file
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# control AI mode
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


# find correct microphone (Auto selecting the microphone)
def get_mic_index():

    # get all connected microphone names
    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):

        # convert microphone name to lowercase
        # helps detect more Realtek microphone variations
        mic_name = name.lower()

        # auto detect Realtek microphones
        #
        # works for:
        # - Realtek HD Audio
        # - Realtek(R) Audio
        # - Microphone Array
        # - laptop microphones
        if "realtek" in mic_name:
            return i

        # fallback for generic microphone arrays
        if "microphone" in mic_name:
            return i

    return None


# take voice command
# take voice command
def takeCommand():

    # create speech recognizer object
    r = sr.Recognizer()

    # energy threshold — controls microphone sensitivity
    # lower value  → hears quieter voice easier
    # higher value → ignores more background noise
    # increase (400–600) if:
    # - fan noise triggers false listening
    # - keyboard sounds activate microphone
    # decrease (100–250) if:
    # - Nexaura is not detecting your voice
    # - microphone volume is low
    # common range:
    # 150 → quiet room
    # 300 → balanced
    # 500+ → noisy room
    #
    # 200 works very well for Indian accents
    # because softer pronunciations get detected easier
    r.energy_threshold = 200

    # dynamic energy threshold
    #
    # True  → automatically adjusts microphone sensitivity
    # False → uses fixed threshold value above
    #
    # True is recommended for:
    # - Indian English accents
    # - changing voice volume
    # - noisy environments
    r.dynamic_energy_threshold = True

    # pause threshold
    #
    # controls how long Nexaura waits
    # before assuming you stopped speaking
    #
    # lower value  → faster response
    # higher value → allows longer pauses while speaking
    #
    # 1.2 works well for Indian English speech pattern
    r.pause_threshold = 1.2

    mic_index = get_mic_index()

    # return empty string if no microphone found
    if mic_index is None:
        print("No microphone found")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            # noise calibration duration in seconds
            # increase if:
            # - room is noisy
            # - fan/AC noise exists
            # decrease if:
            # - room is quiet
            # - you want faster listening
            # recommended:
            # 0.5 → quiet room
            # 1.0 → balanced
            # 2.0 → noisy room
            #
            # 2 seconds recommended for better
            # Indian accent recognition accuracy
            r.adjust_for_ambient_noise(source, duration=2)

            print("Listening...")

            # ── LISTENING TIME SETTINGS ──────────────────────────────────────────#
            # timeout          → seconds Nexaura waits for you to START speaking    #
            #                    increase if you need more time before you begin   #
            #                    decrease for faster timeout                       #
            #                                                                      #
            # phrase_time_limit → seconds Nexaura listens after you START speaking  #
            #                    increase if your commands are long                #
            #                    decrease if you want faster response              #
            #                                                                      #
            # recommended values:                                                  #
            # timeout=3  → fast users                                              #
            # timeout=5  → normal usage                                            #
            # timeout=8+ → slow speaking users                                     #
            #                                                                      #
            # phrase_time_limit=3  → short commands                                #
            # phrase_time_limit=5  → balanced                                      #
            # phrase_time_limit=10+ → long AI conversations                        #
            #
            # slightly increased phrase limit
            # helps Indian English sentence completion
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            # ─────────────────────────────────────────────────────────────────────#

            print("Recognizing...")

            # convert voice into text using Google Speech Recognition
            # 'en-IN' → Indian English
            # 'en-US' → American English
            # 'en-GB' → British English
            #
            # en-IN gives best results for:
            # - Indian pronunciation
            # - Hinglish words
            # - Indian names
            # - mixed Indian English speech
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

    # websites list (you can add more sites)
    # format:
    # ["spoken name", "website url"]
    # example:
    # saying "open youtube"
    # opens youtube website
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["github", "https://github.com/Sam-Dev-161127"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["x", "https://www.x.com"],
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

    # Songs List
    # Note: Your song file path/address will be different from my PC path.
    # Change the path according to where your songs are stored on your computer.
    # supported formats:
    # .mp3 .wav .flac .aac .ogg
    # example:
    # r"D:\Music\song.mp3"
    songs = [
        ["majboor", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Majboor.mp3"],
        ["cornfield", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Cornfield Chase.mp3"],
        ["downfall", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Downfall.mp3"]
    ]

    # Games List
    # Note: Your game shortcut path/address will be different from my PC path.
    # Change the path according to where your games or shortcuts are stored.
    # recommended:
    # use desktop shortcut (.lnk)
    # instead of direct .exe file path
    games = [
        ["valorant", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\VALORANT.lnk"],
        ["epic games", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Epic Games Launcher.lnk"],
        ["genshin impact", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Genshin Impact.lnk"],
        ["steam", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Steam.lnk"]
    ]

    # Apps List
    # Note: Your application shortcut path/address will be different from my PC path.
    # Change the path according to where your apps or shortcuts are stored.
    # format:
    # ["spoken app name", "shortcut path"]
    Apps = [
        ["word", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Word.lnk"],
        ["powerpoint", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\powerpoint.lnk"],
        ["excel", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\excel.lnk"],
        ["opera", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Opera GX Browser .lnk"],
        ["telegram", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Telegram Desktop - Shortcut.lnk"],
        ["whatsapp", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\WhatsApp - Shortcut.lnk"],
        ["instagram", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Instagram - Shortcut.lnk"],
        ["chat gpt", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\ChatGPT - Shortcut.lnk"],
        ["claude", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Claude - Shortcut.lnk"]
    ]

    # infinite loop for continuous listening
    # Nexaura keeps running until:
    # - terminal is closed
    # - program is stopped
    # - PC shuts down
    while True:

        query = takeCommand()

        # skip loop if nothing was heard
        if query == "":
            continue

        command_matched = False

        # handle AI commands first
        #
        # important:
        # AI commands should run before normal commands
        if useAI(query):
            continue

        # open websites — sayAndWait so Nexaura finishes speaking before browser opens
        for site in sites:
            if f"open {site[0]}" in query:
                sayAndWait("Opening " + site[0])
                webbrowser.open(site[1])
                command_matched = True
                break  # ← FIX: stop after first match

        # play songs — sayAndWait so voice fully finishes before song starts playing
        for song in songs:
            if f"play {song[0]}" in query:
                sayAndWait("Playing " + song[0])
                os.startfile(song[1])
                command_matched = True
                break  # ← FIX: stop after first match

        # open games — sayAndWait so Nexaura finishes speaking before game launches
        for game in games:
            if f"open {game[0]}" in query:
                sayAndWait("Opening " + game[0])
                os.startfile(game[1])
                command_matched = True
                break  # ← FIX: stop after first match

        # open apps — sayAndWait so Nexaura finishes speaking before app launches
        for app in Apps:
            if f"open {app[0]}" in query:
                sayAndWait("Opening " + app[0])
                os.startfile(app[1])
                command_matched = True
                break  # ← FIX: stop after first match

        # tell current time
        if "what time is it" in query:
            now = datetime.datetime.now()

            # time formatting codes
            #
            # %I → hour (12-hour format)
            # %H → hour (24-hour format)
            # %M → minutes
            # %S → seconds
            # %p → AM/PM
            #
            # example:
            # 09:45 PM
            hour = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm = now.strftime("%p")
            sayAndWait(f"The time is {hour}:{minute} {am_pm}")

            command_matched = True

        # tell current date
        if "what date is it" in query:
            now = datetime.datetime.now()

            # date formatting codes
            #
            # %A → full weekday name
            # %d → day number
            # %B → full month name
            # %Y → full year
            #
            # example:
            # Monday, 11 May 2026
            day_name = now.strftime("%A")
            day = now.strftime("%d")
            month = now.strftime("%B")
            year = now.strftime("%Y")
            sayAndWait(f"Today is {day_name}, {day} {month} {year}")

            command_matched = True

        # fallback AI if AI mode is enabled
        #
        # if no command matched,
        # AI handles the conversation
        if not command_matched and ai_enabled:
            aiChat(query)

# Follow Me

# GitHub   : https://github.com/Sam-Dev-161127
# LinkedIn : https://www.linkedin.com/in/sameer-patra-2b17a83a7
# X (Twitter) : https://x.com/Sam_Dev_161127
# Instagram : https://www.instagram.com/sam.dev.161127
# Telegram  : https://t.me/Sameer161127


