import cv2
import pandas as pd
import os

from src.camera  import Camera
from src.tracker import PersonTracker
from src.counter import PeopleCounter
from src.utils   import draw_ui
from config      import FRAME_WIDTH, FRAME_HEIGHT

cam     = Camera()
tracker = PersonTracker()
counter = PeopleCounter()

frame_skip  = 2
frame_count = 0
log_data    = []
os.makedirs("data", exist_ok=True)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        boxes, ids = tracker.track(frame)

        total, current, entered, exited = counter.update(boxes, ids)

        annotated = draw_ui(
            frame.copy(),
            total, current, entered, exited,
            boxes=boxes,
            ids=ids,
            pending=counter.pending,
        )

        log_data.append({
            "total":   total,
            "current": current,
            "entered": entered,
            "exited":  exited,
        })
        if len(log_data) > 10000:
            log_data.pop(0)

        cv2.imshow("Employee Tracker PRO", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print("Error:", e)

finally:
    pd.DataFrame(log_data).to_csv("data/logs.csv", index=False)
    cam.release()
    cv2.destroyAllWindows()
