import subprocess
import sys
def start_main_script_as_subprocess():
    try:
        # Change the path to the location of your main_script.py
        main_script_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\video_recorder2.py"
        spectrogram_radar_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\spectrogramGeneratorListener.py"
        spectrogram_video_path = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\videoGeneratorListener.py"
        #subprocess.Popen(["python", main_script_path])
        subprocess.Popen(["python", spectrogram_radar_path])
        subprocess.Popen(["python", spectrogram_video_path])
    except Exception as e:
        print("Error:", e)




if __name__ == '__main__':    
    start_main_script_as_subprocess()

    
