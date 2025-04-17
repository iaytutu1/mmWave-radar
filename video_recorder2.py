#!/usr/bin/env python
# -*- coding: utf-8 -*-
# VideoRecorder.py

from __future__ import print_function, division
import numpy as np
import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import datetime
import shutil

class VideoRecorder():  
    "Video class based on openCV"
    def __init__(self, name="v15_ilhan_temp_temp_video.avi", fourcc="MJPG", sizex=640, sizey=480, camindex=1, fps=30):
        self.open = True
        self.device_index = camindex
        self.fps = fps                  # fps should be the minimum constant rate at which the camera can
        self.fourcc = fourcc            # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (sizex, sizey) # video formats and sizes also depend and vary according to the camera used
        self.video_filename = name
        
        self.video_cap = cv2.VideoCapture(self.device_index,cv2.CAP_DSHOW)

        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    def record(self):
        "Video starts being recorded"
        # counter = 1
        timer_start = time.time()
        timer_current = 0
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                self.video_out.write(video_frame)
                # print(str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current))
                self.frame_counts += 1
                # counter += 1
                # timer_current = time.time() - timer_start
                time.sleep(1/self.fps)
                # gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('video_frame', gray)
                # cv2.waitKey(1)
            else:
                break

    def stop(self):
        "Finishes the video recording therefore the thread too"
        if self.open:
            self.open=False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    def start(self):
        "Launches the video recording function using a thread"
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

class AudioRecorder():
    "Audio class based on pyAudio and Wave"
    def __init__(self, filename="v15_ilhan_temp_temp_audio.wav", rate=44100, fpb=1024, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        "Audio starts being recorded"
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        "Finishes the audio recording therefore the thread too"
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    def start(self):
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

def start_AVrecording(filename="test"):
    global video_thread
    global audio_thread
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()
    audio_thread.start()
    video_thread.start()
    return filename

def start_video_recording(filename="test"):
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()
    return filename

def start_audio_recording(filename="test"):
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()
    return filename

def stop_AVrecording(filename="test"):
    audio_thread.stop() 
    frame_counts = video_thread.frame_counts
    elapsed_time = time.time() - video_thread.start_time
    recorded_fps = frame_counts / elapsed_time
    print("total frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    video_thread.stop() 

    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    # Merging audio and video signal
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected
        print("Re-encoding")
        cmd = "ffmpeg -r " + str(recorded_fps) + " -i v15_ilhan_temp_temp_video.avi -pix_fmt yuv420p -r 6 v15_ilhan_temp_temp_video2.avi"
        subprocess.call(cmd, shell=True)
        print("Muxing")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i v15_ilhan_temp_temp_audio.wav -i v15_ilhan_temp_temp_video2.avi -pix_fmt yuv420p " + f"C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\test_{timestamp}" + ".avi"
        subprocess.call(cmd, shell=True)
    else:
        print("Normal recording\nMuxing")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i v15_ilhan_temp_temp_audio.wav -i v15_ilhan_temp_temp_video.avi -pix_fmt yuv420p " + f"C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\test_{timestamp}" + ".avi"
        subprocess.call(cmd, shell=True)
        print("..")

def file_manager(filename="test"):
    "Required and wanted processing of final files"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if os.path.exists("v15_ilhan_temp_temp_audio.wav"):
        #os.remove("ilhan_temp_audio.wav") 
        shutil.move("v15_ilhan_temp_temp_audio.wav", "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\wavs\\")
        source_folder = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\wavs\\"
        os.rename(source_folder + "v15_ilhan_temp_temp_audio.wav", source_folder + "v15_ilhan_temp_temp_audio_"+ str(timestamp) + ".wav")
    if os.path.exists("v15_ilhan_temp_temp_video.avi"):
        #os.remove("ilhan_temp_video.avi")
        shutil.move("v15_ilhan_temp_temp_video.avi", "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\videos\\")
        source_folder = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\videos\\"
        os.rename(source_folder + "v15_ilhan_temp_temp_video.avi", source_folder + "v15_ilhan_temp_temp_video_" + str(timestamp) + ".avi")
    if os.path.exists("v15_ilhan_temp_temp_video2.avi"):
        #os.remove("ilhan_temp_video2.avi")
        shutil.move("v15_ilhan_temp_temp_video2.avi","C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\videos2\\")
        source_folder = "C:\\ti\\mmwave_studio_02_01_01_00\\mmWaveStudio\\Scripts\\records\\videos2\\"
        os.rename(source_folder + "v15_ilhan_temp_temp_video2.avi", source_folder + "v15_ilhan_temp_temp_video2_" + str(timestamp) + ".avi")
    # if os.path.exists(str(local_path) + "/" + filename + ".avi"):
    #     os.remove(str(local_path) + "/" + filename + ".avi")

if __name__ == '__main__':
    start_AVrecording()
    time.sleep(20)
    stop_AVrecording()
    file_manager()
 