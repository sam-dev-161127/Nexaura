import speech_recognition as sr

# create speech recognizer object
r = sr.Recognizer()

# get all connected microphones
mic_list = sr.Microphone.list_microphone_names()

print("\nAvailable Microphones:\n")

# show all microphones with index number
for i, mic in enumerate(mic_list):
    print(f"{i} : {mic}")

# choose microphone manually
mic_index = int(input("\nEnter microphone index to test: "))

try:

    # use selected microphone
    with sr.Microphone(device_index=mic_index) as source:

        print("\nTesting microphone...")
        print("Speak something...\n")

        # adjust microphone according to room noise
        # 2 seconds gives better calibration
        r.adjust_for_ambient_noise(source, duration=2)

        # microphone sensitivity
        # lower value = more sensitive
        r.energy_threshold = 80

        # automatically adjusts sensitivity
        r.dynamic_energy_threshold = True

        # allows small pauses while speaking
        r.pause_threshold = 1.2

        print("Listening...\n")

        # listen from microphone
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

        print("Recognizing...\n")

        # convert voice into text
        text = r.recognize_google(audio, language="en-IN")

        print("You said:", text)

# user did not speak in time
except sr.WaitTimeoutError:
    print("Listening timeout — no voice detected")

# speech was unclear
except sr.UnknownValueError:
    print("Could not understand audio")

# microphone or device error
except Exception as e:
    print("Error:", e)