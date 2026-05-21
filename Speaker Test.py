"""
Nexaura Speaker + Voice Tester

Features:
- Lists all audio output devices
- Lists all SAPI AI voices
- Lets you select AI voice
- Speaks test lines
- Adjustable volume and speed

Required Libraries:
    pip install pywin32 pycaw

Run:
    python speaker_test.py
"""

from __future__ import annotations

import sys
import time
import argparse

from pathlib import Path
from typing import Iterable, List

# ------------------------------------------#
# CHECK WINDOWS                             #
# ------------------------------------------#

if sys.platform != "win32":
    raise RuntimeError("This script only works on Windows.")

# ------------------------------------------#
# IMPORTS                                   #
# ------------------------------------------#

try:
    import win32com.client
except:
    print("Install pywin32:")
    print("pip install pywin32")
    sys.exit()

try:
    from pycaw.pycaw import AudioUtilities
except:
    print("Install pycaw:")
    print("pip install pycaw")
    sys.exit()

# ------------------------------------------#
# GET SPEAKER                               #
# ------------------------------------------#

def get_speaker():

    return win32com.client.Dispatch("SAPI.SpVoice")

# -------------------------------------------#
# LIST AUDIO DEVICES                         #
# --------------------------------- ---------#

def list_audio_devices():

    print("\n------------------------------------------#")
    print("AUDIO OUTPUT DEVICES                      #")
    print("------------------------------------------#\n")

    devices = AudioUtilities.GetAllDevices()

    found = False

    for i, device in enumerate(devices):

        try:

            name = device.FriendlyName

            if name:

                print(f"[{i}] {name}")
                found = True

        except:
            pass

    if not found:
        print("No audio devices found.")

# ------------------------------------------#
# LIST AI VOICES                            #
# ------------------------------------------#

def list_voices(speaker):

    print("\n------------------------------------------#")
    print("NEXAURA AI VOICES                         #")
    print("------------------------------------------#\n")

    voices = speaker.GetVoices()

    for i in range(voices.Count):

        voice = voices.Item(i)

        print(f"[{i}] {voice.GetDescription()}")

    return voices

# ------------------------------------------#
# SPEAK LINES                               #
# ------------------------------------------#

def speak_lines(
    speaker,
    lines: Iterable[str],
    volume: int = 100,
    rate: int = 0,
    delay: float = 1.0
):

    volume = max(0, min(100, int(volume)))
    rate = max(-10, min(10, int(rate)))

    speaker.Volume = volume
    speaker.Rate = rate

    print("\n------------------------------------------#")
    print("SPEAKING TEST                             #")
    print("------------------------------------------#\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        print(f"Speaking: {line}")

        speaker.Speak(line)

        time.sleep(delay)

# ------------------------------------------#
# LOAD TEXT FILE                            #
# ------------------------------------------#

def load_lines_from_file(path: Path) -> List[str]:

    return [
        l.rstrip("\n")
        for l in path.read_text(encoding="utf-8").splitlines()
    ]

# ------------------------------------------#
# ARGUMENTS                                 #
# ------------------------------------------#

def parse_args():

    parser = argparse.ArgumentParser(
        description="Nexaura Speaker + Voice Tester"
    )

    parser.add_argument(
        "--volume",
        type=int,
        default=100,
        help="Volume 0-100"
    )

    parser.add_argument(
        "--rate",
        type=int,
        default=0,
        help="Voice speed -10 to 10"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between lines"
    )

    parser.add_argument(
        "--voice",
        type=int,
        default=0,
        help="Voice index"
    )

    parser.add_argument(
        "--file",
        type=Path,
        help="Optional text file"
    )

    return parser.parse_args()

# ------------------------------------------#
# MAIN                                      #
# ------------------------------------------#

def main():

    args = parse_args()

    print("\nInitializing Nexaura Audio System...\n")

    # Create speaker
    speaker = get_speaker()

    # Show audio devices
    list_audio_devices()

    # Show voices
    voices = list_voices(speaker)

    # ------------------------------------------#
    # SELECT VOICE                              #
    # ------------------------------------------#

    try:

        speaker.Voice = voices.Item(args.voice)

        selected_voice = voices.Item(args.voice).GetDescription()

        print(f"\nSelected Voice: {selected_voice}")

    except:

        print("\nInvalid voice index.")
        print("Using default voice.\n")

    # ------------------------------------------#
    # DEFAULT TEST LINES                        #
    # ------------------------------------------#

    default_lines = [
        "Hello Sam.",
        "I am Nexaura AI.",
        "Speaker test successful.",
        "All systems are working perfectly."
    ]

    # Load custom file if provided
    if args.file:

        try:

            lines = load_lines_from_file(args.file)

        except Exception as e:

            print(f"Error reading file: {e}")

            lines = default_lines

    else:

        lines = default_lines

    # ------------------------------------------#
    # START SPEAKING                            #
    # ------------------------------------------#

    speak_lines(
        speaker=speaker,
        lines=lines,
        volume=args.volume,
        rate=args.rate,
        delay=args.delay
    )

    print("\n------------------------------------------#")
    print("TEST COMPLETED                            #")
    print("------------------------------------------#\n")

# ------------------------------------------#
# START PROGRAM                             #
# ------------------------------------------#

if __name__ == "__main__":

    main()