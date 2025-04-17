import subprocess
import sys
def start_main_script_as_subprocess():
    try:
        # Change the path to the location of your main_script.py
        print("start_main_script_as_subprocess.......................")
        print(sys.argv[1])

        print(sys.argv[0])
        arg1 = sys.argv[1]
        print(f"Received from Lua: {arg1}")

        spectrogram_radar_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\play_wavs.py"
        # spectrogram_video_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\videoGeneratorListener.py"
        #subprocess.Popen(["python", main_script_path])
        subprocess.Popen(["python", spectrogram_radar_path, arg1])
        # subprocess.Popen(["python", spectrogram_video_path])
    except Exception as e:
        print("Error:", e)




if __name__ == '__main__':    
    print(".............start_main_script_as_subprocess.......................")
    start_main_script_as_subprocess()

    
