import simpleaudio as sa
import os
def get_wav_files(directory):
    """Returns a list of all WAV files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.wav')]
class AudioPlayer:
    def __init__(self):
        self.play_obj = None

    def play(self, audiofile):
       
        wave_obj = sa.WaveObject.from_wave_file(audiofile)
        self.play_obj = wave_obj.play()
    
    def is_done(self):
        if self.play_obj:
            return not self.play_obj.is_playing()
        return True

player = AudioPlayer()
directory = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\audio_chunks\\s"
wav_files = get_wav_files(directory)
# sorted_wav_files = sorted(wav_files, key=lambda x: [int(part) if part.isdigit() else part for part in x.split('_')])    # Play each WAV file for exactly 2 seconds
for wav_file in wav_files:
    file_path = os.path.join(directory, wav_file)
    player.play(file_path)
    if player.is_done():
        player.play(file_path)