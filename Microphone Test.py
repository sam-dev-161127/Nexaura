"""
Fast Nexaura Microphone Tester

Features:
- Lists all microphones
- Fast microphone response
- Faster speech recognition
- Better for AI assistants
- Low delay listening

Required Libraries:
    pip install SpeechRecognition pyaudio

Run:
    python microphone_test.py
"""

import speech_recognition as sr

# ------------------------------------------#
# CREATE RECOGNIZER                         #
# ------------------------------------------#

r = sr.Recognizer()

# Fast AI assistant settings
r.energy_threshold = 120
r.dynamic_energy_threshold = False
r.pause_threshold = 0.6
r.phrase_threshold = 0.2
r.non_speaking_duration = 0.3

# ------------------------------------------#
# SHOW ALL MICROPHONES                      #
# ------------------------------------------#

print("\n------------------------------------------#")
print("AVAILABLE MICROPHONES                     #")
print("------------------------------------------#\n")

mic_list = sr.Microphone.list_microphone_names()

for i, mic in enumerate(mic_list):

    print(f"[{i}] {mic}")

# ------------------------------------------#
# SELECT MICROPHONE                         #
# ------------------------------------------#

try:

    mic_index = int(
        input("\nEnter microphone index: ")
    )

except:

    print("\nInvalid microphone index.")
    exit()

# ------------------------------------------#
# START MICROPHONE TEST                     #
# ------------------------------------------#

try:

    with sr.Microphone(device_index=mic_index) as source:

        print("\n------------------------------------------#")
        print("FAST MICROPHONE TEST                      #")
        print("------------------------------------------#\n")

        print("Calibrating microphone...\n")

        # Faster background noise adjustment
        r.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        print("Speak now...\n")

        # Fast listening
        audio = r.listen(
            source,
            timeout=3,
            phrase_time_limit=5
        )

        print("Recognizing speech...\n")

        # Speech recognition
        text = r.recognize_google(
            audio,
            language="en-IN"
        )

        print("------------------------------------------#")
        print("VOICE RECOGNIZED                          #")
        print("------------------------------------------#\n")

        print("You said:")
        print(text)

# ------------------------------------------#
# ERRORS                                    #
# ------------------------------------------#

except sr.WaitTimeoutError:

    print("\nNo voice detected")

except sr.UnknownValueError:

    print("\nCould not understand audio")

except OSError:

    print("\nMicrophone device error")

except Exception as e:

    print("\nError:", e)

# ------------------------------------------#
# END                                       #
# ------------------------------------------#

print("\n------------------------------------------#")
print("MIC TEST COMPLETED                        #")
print("------------------------------------------#")