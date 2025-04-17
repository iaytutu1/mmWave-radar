import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
import mmwave.dsp as dsp
from mmwave.dataloader import DCA1000
import matplotlib.pyplot as plt

# Global variables for the first listener
input_directory = r'C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\PostProc\vowels_correct\radar_watcher_directory'  # Replace with your input directory path
output_directory = r'C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\PostProc\vowels_correct\radar_visiualize_directory'  # Replace with your output directory path
spectrogram_size_kb = 512  # Size of the .bin file in kilobytes

class SpectrogramGenerator(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith('.bin'):
            # Ignore directories and non-.bin files
            return

        file_path = event.src_path
        print(f"New .bin file created: {file_path}")
        
        total_size_kb = 512  # total size in kilobytes
        total_size = total_size_kb * 1024  # convert to bytes
        
        # Wait for the file to be ready (timeout after 10 seconds)
        # timeout = 10  # seconds
        # start_time = time.time()
        while not is_file_ready(file_path, total_size):
            time.sleep(1)
            # if time.time() - start_time > timeout:
                # print(f"Timeout waiting for file readiness: {file_path}")
                # return

        # Process the .bin file and generate spectrogram
        generate_spectrogram(file_path)

def is_file_ready(file_path, total_size):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            return False

        # Check if the file size is equal to the total size
        current_size = os.path.getsize(file_path)
        return current_size == total_size

    except Exception as e:
        print(f"Error checking file readiness: {e}")
        return False

def generate_spectrogram(bin_file_path):
    # Your existing code for processing a single frame
    adc_data = np.fromfile(bin_file_path,  dtype=np.uint16)
    numChirpsPerFrame, numFrames, numRxAntennas, numADCSamples = 128, 1, 4, 256

    adc_data = adc_data.reshape(numFrames, -1)
    adc_data = np.apply_along_axis(DCA1000.organize, 1, adc_data, num_chirps=numChirpsPerFrame,
                                   num_rx=numRxAntennas, num_samples=numADCSamples)

    print("Data Loaded!: with shape {}".format(adc_data.shape))

    radar_cube = dsp.range_processing(adc_data[0])
    det_matrix, aoa_input = dsp.doppler_processing(radar_cube, num_tx_antennas=2, interleaved=False, clutter_removal_enabled=False)
    det_matrix_vis = np.fft.fftshift(det_matrix, axes=1)
    min_val = det_matrix_vis.min()
    max_val = det_matrix_vis.max()

    # Normalize the matrix for visualization
    normalized_matrix = np.round((det_matrix_vis - min_val) / (max_val - min_val) * 255)
    normalized_matrix = normalized_matrix.astype(np.uint8)

    # Save the spectrogram as a .png file
    output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(bin_file_path))[0]}.png")    
    plt.figure(figsize=(8, 6))
    plt.imshow(normalized_matrix.T, aspect='auto')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(output_file_path)
    plt.close()

    print(f"Spectrogram saved: {output_file_path}")

# Start the first listener
def start_spectrogram_listener():
    event_handler = SpectrogramGenerator()
    observer = Observer()
    observer.schedule(event_handler, path=input_directory, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Call this function to start the first listener
start_spectrogram_listener()
