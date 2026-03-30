import cv2
import time

prev_time = 0

def draw_ui(frame, total, current):
    global prev_time

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (260, 120), (50, 50, 50), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    cv2.rectangle(frame, (10, 10), (260, 120), (0, 255, 255), 2)


    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(frame, f"Total: {total}", (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(frame, f"Live: {current}", (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame