import pywinauto
import time
import subprocess
import os
import datetime


# def win_record(duration):
    # subprocess.run('start microsoft.windows.camera:', shell=True)  # open camera app

    # # focus window by getting handle using title and class name
    # # subprocess call opens camera and gets focus, but this provides alternate way
    # # t, c = 'Camera', 'ApplicationFrameWindow'
    # # handle = pywinauto.findwindows.find_windows(title=t, class_name=c)[0]
    # # # get app and window
    # # app = pywinauto.application.Application().connect(handle=handle)
    # # window = app.window(handle=handle)
    # # window.set_focus()  # set focus
    # time.sleep(2)  # have to sleep

    # # take control of camera window to take video
    # desktop = pywinauto.Desktop(backend="uia")
    
    # cam = desktop['Camera']
    # # cam.print_control_identifiers()
    # # make sure in video mode
    # if cam.child_window(title="Switch to Video mode", auto_id="CaptureButton_1", control_type="Button").exists():
        # cam.child_window(title="Switch to Video mode", auto_id="CaptureButton_1", control_type="Button").click()
    # time.sleep(1)
    # # start then stop video
    # cam.child_window(title="Take Video", auto_id="CaptureButton_1", control_type="Button").click()
    # time.sleep(duration+2)
    # cam.child_window(title="Stop taking Video", auto_id="CaptureButton_1", control_type="Button").click()

    # # retrieve vids from camera roll and sort
    # dir = 'C:\\Users\\yapaynazar\\Videos\\Captures'
    # all_contents = list(os.listdir(dir))
    # vids = [f for f in all_contents if "_Pro.mp4" in f]
    # vids.sort()
    # vid = vids[-1]  # get last vid
    # # compute time difference
    # vid_time = vid.replace('WIN_', '').replace('_Pro.mp4', '')
    # vid_time = datetime.datetime.strptime(vid_time, '%Y%m%d_%H_%M_%S')
    # now = datetime.datetime.now()
    # diff = now - vid_time
    # # time different greater than duration plus 1 minute, assume something wrong & quit
    # if diff.seconds > (duration * 60 + 60):
        # quit()
    # subprocess.run('Taskkill /IM WindowsCamera.exe /F', shell=True)  # close camera app
    # print('Recorded successfully!')


# win_record(2)

# from pywinauto import Application


# from pywinauto.keyboard import send_keys

# subprocess.run('start microsoft.windows.camera:', shell=True)  # open camera app

# desktop = pywinauto.Desktop(backend="uia")

# cam = desktop['Camera']


# cam.send_chars("{ENTER}")
# cam.child_window(title="Take Video", auto_id="CaptureButton_1", control_type="Button").click()



import cv2
import os
import datetime
import sys
class CameraRecorder:
    def __init__(self, is_exit=""):
        # Create the records folder if it doesn't exist
        if not os.path.exists('records'):
            os.makedirs('records')
        
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
       
                
        # Define the video codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = f"records/video_{timestamp}.mp4"
        self.out = cv2.VideoWriter(self.output_file, fourcc, 20.0, (640, 480))

    def record_video(self, is_exit="" ):
        while True:
            if is_exit == "exit":
                break
            # Read each frame from the camera
            ret, frame = self.cap.read()

            # Write the frame to the video file
            self.out.write(frame)

            # Display the resulting frame
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) and is_exit == "exit":
                break
           
        if is_exit != "exit":
            # Release the resources
            self.cap.release()
            self.out.release()
            cv2.destroyAllWindows()
        else:
            self.cap.release()

if __name__ == "__main__":

    args = sys.argv[1:]
    print(args)
    # Create an instance of CameraRecorder
    recorder = CameraRecorder(is_exit="exit")
    if len(args) > 0 : 
    # Call the record_video method
        recorder.record_video(is_exit = args[1])
    else: 
        recorder.record_video()