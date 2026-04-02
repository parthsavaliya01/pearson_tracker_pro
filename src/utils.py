import cv2
import time
from config import LINE_POSITION

prev_time = 0

def draw_ui(frame, total, current, entered, exited):
    global prev_time

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    # DRAW LINE
    cv2.line(frame, (LINE_POSITION, 0), (LINE_POSITION, frame.shape[0]), (255, 239, 51), 2)

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (300, 160), (50, 50, 50), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    cv2.rectangle(frame, (10, 10), (300, 160), (0, 255, 255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(frame, f"Total: {total}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Live: {current}", (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, f"IN: {entered}", (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.putText(frame, f"OUT: {exited}", (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 100), 2)

    return frame