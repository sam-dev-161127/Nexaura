import win32com.client
import time

# create Windows text-to-speech speaker
speaker = win32com.client.Dispatch("SAPI.SpVoice")

print("Testing speaker...\n")

# set speaker volume
# range:
# 0   → mute
# 100 → maximum volume
speaker.Volume = 100

# set speaking speed
# negative = slower
# positive = faster
# 0 = normal
speaker.Rate = 0

# test sentences
tests = [
    "Hello Sam.",
    "I am Nex Aura AI.",
    "Speaker test successful.",
    "Your AI assistant is working perfectly."
]

# speak all test sentences
for line in tests:

    print("Speaking:", line)

    # speak text
    speaker.Speak(line)

    # small delay between lines
    time.sleep(1)

print("\nSpeaker test completed.")