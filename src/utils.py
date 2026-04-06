import cv2
import time
from config import LINE_POSITION, INSIDE_DIRECTION, EDGE_MARGIN, FRAME_WIDTH

prev_time = 0


def draw_ui(frame, total, current, entered, exited,
            boxes=None, ids=None, pending=None):
    global prev_time

    curr_time = time.time()
    fps       = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    h, w = frame.shape[:2]
    line = LINE_POSITION

    # ── edge confirm zones (thin red lines) ───────────────────────────
    cv2.line(frame, (EDGE_MARGIN + 30, 0), (EDGE_MARGIN +30, h), (0, 0, 200), 1)
    cv2.line(frame, (FRAME_WIDTH - EDGE_MARGIN, 0),
             (FRAME_WIDTH - EDGE_MARGIN, h), (0, 0, 200), 1)

    # ── tripwire line (yellow) ────────────────────────────────────────
    cv2.line(frame, (line, 0), (line, h), (0, 220, 255), 2)

    # ── side labels ───────────────────────────────────────────────────
    if INSIDE_DIRECTION == 'right':
        left_label, right_label = "OUTSIDE", "INSIDE"
        left_color  = (0,   220, 100)   # green  = outside (door/corridor)
        right_color = (255, 140,   0)   # orange = inside  (office)

    cv2.putText(frame, left_label,  (max(line - 115, 4), h - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, left_color,  2)
    cv2.putText(frame, right_label, (line + 8,           h - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, right_color, 2)

    # ── bounding boxes ────────────────────────────────────────────────
    if boxes is not None and ids is not None:
        for box, tid in zip(boxes, ids):
            x1, y1, x2, y2 = map(int, box)
            tid = int(tid)
            fx  = int((x1 + x2) / 2)

            pend = (pending or {}).get(tid)

            if pend == 'enter':
                color = (0, 255, 255)    # cyan  = pending entry
                label = f"ID{tid} IN?"
            elif pend == 'exit':
                color = (0, 100, 255)    # orange = pending exit
                label = f"ID{tid} OUT?"
            elif fx < line:
                color = left_color
                label = f"ID{tid}"
            else:
                color = right_color
                label = f"ID{tid}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (fx, y2), 6, color, -1)
            cv2.putText(frame, label, (x1, max(y1 - 8, 14)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    # ── stats panel ───────────────────────────────────────────────────
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (310, 175), (30, 30, 30), -1)
    frame = cv2.addWeighted(overlay, 0.65, frame, 0.35, 0)
    cv2.rectangle(frame, (10, 10), (310, 175), (0, 255, 255), 2)

    cv2.putText(frame, f"FPS:   {int(fps)}",  (20,  38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Total: {total}",      (20,  68),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,   0), 2)
    cv2.putText(frame, f"Live:  {current}",    (20,  98),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
    cv2.putText(frame, f"IN:    {entered}",    (20, 128),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255,  0), 2)
    cv2.putText(frame, f"OUT:   {exited}",     (20, 158),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

    return frame