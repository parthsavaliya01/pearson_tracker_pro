from ultralytics import YOLO

class PersonTracker:
    def __init__(self):
        self.model = YOLO("models/yolov8n.pt")

    def track(self, frame):
        results = self.model.track(
    frame,
    persist=True,
    classes=[0],
    conf=0.4,     
    iou=0.5,
    tracker="bytetrack.yaml",
    imgsz=640  
)
        return results