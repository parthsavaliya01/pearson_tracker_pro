from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort


class PersonTracker:
    def __init__(self):
        self.model = YOLO("models/yolov8n.pt")

        self.tracker = DeepSort(
            max_age=60,
            n_init=3,
            max_cosine_distance=0.25,
            nn_budget=100,
        )

    def track(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []

        if results.boxes is not None:
            boxes   = results.boxes.xyxy.cpu().numpy()
            scores  = results.boxes.conf.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy()

            for box, score, cls in zip(boxes, scores, classes):
                if int(cls) != 0:
                    continue
                if score < 0.40:
                    continue
                x1, y1, x2, y2 = box
                detections.append(([x1, y1, x2 - x1, y2 - y1], float(score), 'person'))

        tracks = self.tracker.update_tracks(detections, frame=frame)

        boxes_out = []
        ids_out   = []

        for track in tracks:
            if not track.is_confirmed():
                continue
            if track.time_since_update > 1:
                continue

            x1, y1, x2, y2 = track.to_ltrb()
            x1 = max(0.0, x1)
            y1 = max(0.0, y1)

            boxes_out.append([x1, y1, x2, y2])
            ids_out.append(track.track_id)

        return boxes_out, ids_out
