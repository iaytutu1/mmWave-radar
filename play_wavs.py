import os
import time
import wave
import simpleaudio as sa
import re
import sys
def get_wav_files(directory):
    """Returns a list of all WAV files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.wav')]

def play_wav_for_duration(idx, file_path, total_duration=2):
    """Plays a single WAV file for exactly total_duration seconds, looping if necessary."""
    try:
        # Load the WAV file using wave and simpleaudio
        with wave.open(file_path, 'rb') as wav_file:
            wav_data = wav_file.readframes(wav_file.getnframes())
            sample_rate = wav_file.getframerate()
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()

            # Create a playable audio object
            audio_obj = sa.play_buffer(wav_data, num_channels, sample_width, sample_rate)

            # Play the file
            playback_start_time = time.time()
            while time.time() - playback_start_time < total_duration:
                # Replay the sound if the duration is longer than the file's length
                if not audio_obj.is_playing():
                    audio_obj = sa.play_buffer(wav_data, num_channels, sample_width, sample_rate)
                time.sleep(0.01)  # Small delay to avoid high CPU usage

            audio_obj.stop()  # Stop the audio if it's still playing after 2 seconds

    except Exception as e:
        print(f"Error occurred while playing {file_path}: {e}")

if __name__ == "__main__":
  
    # Directory containing the WAV files
    directory = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\audio_chunks\p"
    
    # Get all WAV files in the directory
    wav_files = get_wav_files(directory)
    
    if not wav_files:
        print(f"No WAV files found in directory: {directory}")
        sys.exit(1)

    sorted_wav_files = sorted(wav_files, key=lambda x: [int(part) if part.isdigit() else part for part in x.split('_')])    # Play each WAV file for exactly 2 seconds

#    for idx, wav_file in enumerate(sorted_wav_files):
#        file_path = os.path.join(directory, wav_file)
#        print(f"Playing {wav_file} for 2 seconds...")
#        play_wav_for_duration(idx, file_path, total_duration=2)
#        print(f"Waiting 5 seconds before playing the next file...")
#        time.sleep(5)

    arg1 = sys.argv[1]
    idx = int(arg1) - 1
    file_path = os.path.join(directory, sorted_wav_files[idx])
    
    print(f"Playing {sorted_wav_files[idx]} for 2 seconds...")
    play_wav_for_duration(idx, file_path, total_duration=2)
    #process.terminate()  # Use process.kill() if you need to forcefully kill it
