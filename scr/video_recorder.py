import cv2
import numpy as np
from picamera2 import Picamera2
from collections import deque


class VideoRecorder:
    def __init__(self, width, height, fps, buffer_seconds):
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_buffer = deque(maxlen=buffer_seconds * fps)
        self.camera = Picamera2()
        self.camera.preview_configuration.main.size = (self.width, self.height)
        self.camera.preview_configuration.main.format = "RGB888"
        self.camera.preview_configuration.controls.FrameRate = fps
        self.camera.configure("preview")
        self.camera.start()

    def capture_frame(self):
        frame = self.camera.capture_array()
        self.frame_buffer.append(frame)
        return frame

    def save_video(self):
        video_file = "video.h264"
        out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*"X264"), self.fps, (self.width, self.height))

        for frame in self.frame_buffer:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()
        return video_file