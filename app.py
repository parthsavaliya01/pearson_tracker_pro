import cv2
import pandas as pd
import os
from src.camera import Camera
from src.tracker import PersonTracker
from src.counter import PeopleCounter
from src.utils import draw_ui
from config import FRAME_WIDTH, FRAME_HEIGHT

cam = Camera()
tracker = PersonTracker()
counter = PeopleCounter()

frame_skip = 2
frame_count = 0

log_data = []
os.makedirs("data", exist_ok=True)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame_count += 1

        # 🔥 Skip early (performance fix)
        if frame_count % frame_skip != 0:
            continue

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        results = tracker.track(frame)
        annotated = results[0].plot()

        if results[0].boxes is not None and len(results[0].boxes) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy()

            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.cpu().numpy()
            else:
                ids = list(range(len(boxes)))
        else:
            boxes = []
            ids = []

        # ✅ FIRST calculate values
        total, current = counter.update(boxes, ids)

        # ✅ THEN draw UI
        annotated = draw_ui(annotated, total, current)

        log_data.append({
            "total": total,
            "current": current
        })

        if len(log_data) > 10000:
            log_data.pop(0)

        cv2.imshow("Employee Tracker PRO", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print("Error:", e)

finally:
    df = pd.DataFrame(log_data)
    df.to_csv("data/logs.csv", index=False)

    cam.release()
    cv2.destroyAllWindows()