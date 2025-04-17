import os
import cv2
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Global variables for the second listener
display_window_name = 'Real-Time Display'
frame_interval = 0.1  # Interval between frames in seconds
file_size_threshold_kb = 300  # Threshold for stable file size in kilobytes
initial_delay_seconds = 3


class RealTimeDisplay(FileSystemEventHandler):
    def __init__(self):
        self.frame_queue = []

    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith('.png'):
            # Ignore directories and non-.png files
            return

        file_path = event.src_path
        print(f"New .png file created: {file_path}")

        # Process the .png file and add it to the display queue

        #print(file_path)
        print("BURAYA geldi 0")
        stable_file_size = self.wait_for_stable_file_size(file_path)
        if stable_file_size:
            frame = cv2.imread(file_path)
            if frame is not None:
                self.frame_queue.append(frame)
                
    def wait_for_stable_file_size(self, file_path, timeout_sec=10):
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                initial_size = os.path.getsize(file_path)
                time.sleep(0.01)
                current_size = os.path.getsize(file_path)
                if initial_size == current_size and current_size >= (file_size_threshold_kb * 1024):
                    return True
            return False
        



def start_real_time_display():
    display_handler = RealTimeDisplay()
    observer = Observer()
    observer.schedule(display_handler, path=r'C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\PostProc\vowels_correct\radar_visiualize_directory', recursive=False)

    observer.start()
    print("Waiting for observer and first file...")
    while not display_handler.frame_queue:
        time.sleep(1)
    
    print("Initial delay after first file detection...")
    time.sleep(3)

    print("Initial delay completed. Starting real-time display.")
    print("BURAYA geldi 1")
    try:
        while True:
            if display_handler.frame_queue:
                frame = display_handler.frame_queue.pop(0)
                if frame is not None:
                        print("BURAYA geldi 2")
                        WINDOW_NAME = "win"
                        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                        image = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_NEAREST)    
                        cv2.startWindowThread()

                        cv2.imshow(WINDOW_NAME, image)
                        
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                time.sleep(frame_interval)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    cv2.destroyAllWindows()
    #cv2.waitKey(1)  # Ensure the window stays open until a key is pressed

# Call this function to start the real-time display listener
start_real_time_display()
