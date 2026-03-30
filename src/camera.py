import cv2
from config import VIDEO_SOURCE
import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_SOURCE, cv2.CAP_FFMPEG)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise Exception("Cannot open video source")

    def read(self):
        for _ in range(2):
            self.cap.grab()

        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()