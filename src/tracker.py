import logging
from pathlib import Path

import cv2
from ultralytics import YOLO

from config import DETECTION_CONFIDENCE, FRAME_HEIGHT, FRAME_WIDTH, IOU_THRESHOLD, MODEL_PATH

logger = logging.getLogger(__name__)


class PersonTracker:
    def __init__(self):
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            model_path = Path("models") / "yolov8n.pt"

        self.model = YOLO(str(model_path))
        self.confidence = DETECTION_CONFIDENCE
        self.iou = IOU_THRESHOLD
        self.imgsz = 320

    def track(self, frame):
        if frame is None:
            return [], []

        resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        try:
            results = self.model.track(
                resized,
                stream=False,
                persist=False,
                conf=self.confidence,
                iou=self.iou,
                imgsz=self.imgsz,
                classes=[0],
                agnostic_nms=True,
                tracker="bytetrack.yaml",
            )
        except Exception as exc:
            logger.warning("Tracking failed: %s", exc)
            return [], []

        if not results:
            return [], []

        result = results[0]
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            return [], []

        xyxy = boxes.xyxy.cpu().numpy()
        classes = boxes.cls.cpu().numpy().astype(int)
        confidences = boxes.conf.cpu().numpy()
        track_ids = getattr(boxes, "id", None)

        if track_ids is None:
            track_ids = list(range(len(xyxy)))
        else:
            track_ids = track_ids.cpu().numpy().astype(int)

        kept_boxes = []
        kept_ids = []

        for box, cls_id, confidence, track_id in zip(xyxy, classes, confidences, track_ids):
            if int(cls_id) != 0:
                continue
            if float(confidence) < self.confidence:
                continue

            x1, y1, x2, y2 = map(float, box)
            kept_boxes.append([x1, y1, x2, y2])
            kept_ids.append(int(track_id))

        return kept_boxes, kept_ids
