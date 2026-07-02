import logging

import cv2

from config import FRAME_HEIGHT, FRAME_WIDTH, VIDEO_SOURCE

logger = logging.getLogger(__name__)


class Camera:
    def __init__(self):
        self.cap = None
        self.error_message = None
        self._open_camera()

    def _open_camera(self) -> None:
        try:
            source = VIDEO_SOURCE
            capture_source = int(source) if str(source).isdigit() else str(source)
            self.cap = cv2.VideoCapture(capture_source)
        except (TypeError, ValueError):
            self.cap = cv2.VideoCapture(str(VIDEO_SOURCE))

        if self.cap is None or not self.cap.isOpened():
            self.error_message = f"Unable to open camera source: {VIDEO_SOURCE}"
            logger.warning(self.error_message)
            return

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    @property
    def is_available(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

    def read(self):
        if not self.is_available:
            return False, None
        ret, frame = self.cap.read()
        return ret, frame

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
