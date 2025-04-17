import cv2
import threading
import time
import numpy as np

# Define the frame directory and output video file
frame_directory = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\testframes"
output_video_file = "output_video.mp4"

# Get the list of frames from the directory
frame_files = ["S1_adc_data_1_Raw_0.bin_1.png", "S1_adc_data_1_Raw_0.bin_2.png", "S1_adc_data_1_Raw_0.bin_3.png", "S1_adc_data_1_Raw_0.bin_4.png"]
frames = [cv2.imread(f"{frame_directory}/{frame}") for frame in frame_files]

# Get the height and width of the frames
height, width, _ = frames[0].shape

# Set up the video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video_file, fourcc, 1.0, (width, height))
print(len(frames))
# Function to write frames to the video
def write_frame_to_video():
    for frame in frames:
        out.write(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.5)  # Simulate some processing time

# Create and start the thread
thread = threading.Thread(target=write_frame_to_video)
thread.start()

# Wait for the thread to finish (you can set a condition to stop the thread)
thread.join()

# Release the video writer
out.release()

# Close all windows
cv2.destroyAllWindows()

print("Video creation complete.")
