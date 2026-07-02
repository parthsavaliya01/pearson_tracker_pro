import asyncio
import logging
import time

import cv2
import numpy as np
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from config import FRAME_HEIGHT, FRAME_WIDTH
from db import get_recent_stats, init_db, insert_stats
from src.camera import Camera
from src.counter import PeopleCounter
from src.tracker import PersonTracker
from src.utils import draw_ui

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("employee_tracker")

app = FastAPI(title="Employee Tracker PRO", version="1.0.0")
templates = Jinja2Templates(directory="templates")
init_db()

latest_stats = {
    "total": 0,
    "current": 0,
    "entered": 0,
    "exited": 0,
    "status": "starting",
    "camera_ok": False,
}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "employee-tracker"}


@app.get("/analytics")
def get_analytics():
    return get_recent_stats()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(latest_stats)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        logger.info("WebSocket closed")
    except Exception as exc:
        logger.exception("WebSocket error: %s", exc)
    finally:
        await websocket.close()


def _build_error_frame(message: str):
    frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    cv2.putText(frame, "Camera unavailable", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.putText(frame, message, (40, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return frame


def generate_frames():
    cam = Camera()
    tracker = PersonTracker()
    counter = PeopleCounter()
    frame_count = 0

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                latest_stats["status"] = "camera_unavailable"
                latest_stats["camera_ok"] = False
                if cam.error_message:
                    latest_stats["message"] = cam.error_message
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + cv2.imencode(".jpg", _build_error_frame(cam.error_message or "Unable to open camera"))[1].tobytes()
                    + b"\r\n"
                )
                time.sleep(0.5)
                continue

            latest_stats["status"] = "tracking"
            latest_stats["camera_ok"] = True
            latest_stats["message"] = "Camera connected"

            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            boxes, ids = tracker.track(frame)
            total, current, entered, exited = counter.update(boxes, ids)

            latest_stats["total"] = total
            latest_stats["current"] = current
            latest_stats["entered"] = entered
            latest_stats["exited"] = exited

            annotated = draw_ui(
                frame.copy(),
                total,
                current,
                entered,
                exited,
                boxes=boxes,
                ids=ids,
                pending=counter.pending,
            )

            frame_count += 1
            if frame_count % 5 == 0:
                insert_stats(total, current, entered, exited)

            success, buffer = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not success:
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )
    except Exception as exc:
        logger.exception("Streaming loop failed: %s", exc)
    finally:
        cam.release()


@app.get("/video")
def video():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
