import subprocess
import os
import time
from pydub import AudioSegment
from pydub.playback import play

# Path to mmWave Studio executable
mmwave_studio_path = r"C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\RunTime\mmWaveStudio.exe"
lua_script_path = r"C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\Scripts\DataCaptureDemo_xWR_ForUltrasuite.lua"

# Start mmWave Studio
subprocess.Popen([mmwave_studio_path])
time.sleep(10)  # Wait for mmWave Studio to launch

# Function to start the radar script using mmWave Studio's environment
def play_wav_and_start_lua(wav_file, lua_script_path):
    try:
        # Load the WAV file
        audio = AudioSegment.from_wav(wav_file)
        duration_ms = len(audio)
        duration_seconds = duration_ms / 1000

        print(f"Playing {os.path.basename(wav_file)} (Duration: {duration_seconds:.2f} seconds)")

        # Load and execute Lua script in mmWave Studio via subprocess (DDE-like interaction)
        radar_process = subprocess.Popen([
            "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\RadarAPI.exe",
            "-s", lua_script_path
        ])

        # Play the audio
        play(audio)
        print("Radar capture started.")

        # Ensure the radar capture runs for the duration of the audio
        time.sleep(duration_seconds)

        # Stop radar capture after WAV file ends
        radar_process.terminate()
        print("Radar capture finished.")

    except Exception as e:
        print("Error:", e)

# Define the directory where WAV files are stored
directory = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\audio_chunks\\b"

# Loop through each WAV file in the directory and start the radar capture
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        wav_file = os.path.join(directory, filename)
        play_wav_and_start_lua(wav_file, lua_script_path)
