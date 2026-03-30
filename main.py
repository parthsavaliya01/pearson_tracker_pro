# # from fastapi import FastAPI
# # from fastapi.responses import StreamingResponse
# # from fastapi.templating import Jinja2Templates
# # from fastapi import Request
# # import cv2

# # from src.camera import Camera
# # from src.tracker import PersonTracker
# # from src.counter import PeopleCounter
# # from src.utils import draw_ui
# # from config import FRAME_WIDTH, FRAME_HEIGHT

# # app = FastAPI()

# # templates = Jinja2Templates(directory="templates")

# # from fastapi import Request

# # @app.get("/")
# # def home(request: Request):
# #     return templates.TemplateResponse("index.html", {"request": request})

# # def generate_frames():
# #     cam = Camera()                 # ✅ moved inside
# #     tracker = PersonTracker()      # ✅ moved inside
# #     counter = PeopleCounter()      # ✅ moved inside

# #     while True:
# #         ret, frame = cam.read()
# #         if not ret:
# #             break

# #         frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

# #         results = tracker.track(frame)
# #         annotated = results[0].plot()

# #         if results[0].boxes is not None and len(results[0].boxes) > 0:
# #             boxes = results[0].boxes.xyxy.cpu().numpy()
# #             ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else list(range(len(boxes)))
# #         else:
# #             boxes, ids = [], []

# #         total, current = counter.update(boxes, ids)

# #         annotated = draw_ui(annotated, total, current)

# #         _, buffer = cv2.imencode('.jpg', annotated)
# #         frame_bytes = buffer.tobytes()

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# # @app.get("/video")
# # def video():
# #     return StreamingResponse(generate_frames(),
# #                              media_type="multipart/x-mixed-replace; boundary=frame")

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import cv2

from src.camera import Camera
from src.tracker import PersonTracker
from src.counter import PeopleCounter
from src.utils import draw_ui
from config import FRAME_WIDTH, FRAME_HEIGHT
from fastapi import WebSocket
from db import insert_stats
import asyncio
from fastapi import WebSocket
import asyncio

# app = FastAPI()

# # ✅ Templates
# templates = Jinja2Templates(directory="templates")

# # ✅ GLOBAL STATS (for dashboard)
# latest_stats = {
#     "total": 0,
#     "current": 0
# }

# # ✅ HOME PAGE
# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     cam = Camera()
#     tracker = PersonTracker()
#     counter = PeopleCounter()

#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             break

#         frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

#         results = tracker.track(frame)

#         if results[0].boxes is not None and len(results[0].boxes) > 0:
#             boxes = results[0].boxes.xyxy.cpu().numpy()
#             ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else list(range(len(boxes)))
#         else:
#             boxes, ids = [], []

#         total, current = counter.update(boxes, ids)

#         await websocket.send_json({
#             "total": total,
#             "current": current
#         })

#         await asyncio.sleep(0.5)


# # ✅ VIDEO STREAM FUNCTION
# def generate_frames():
#     cam = Camera()
#     tracker = PersonTracker()
#     counter = PeopleCounter()

#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             break

#         frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

#         results = tracker.track(frame)
#         annotated = results[0].plot()

#         if results[0].boxes is not None and len(results[0].boxes) > 0:
#             boxes = results[0].boxes.xyxy.cpu().numpy()
#             ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else list(range(len(boxes)))
#         else:
#             boxes, ids = [], []

#         # ✅ UPDATE COUNTER
#         total, current = counter.update(boxes, ids)

#         # ✅ SAVE TO GLOBAL STATS
#         latest_stats["total"] = total
#         latest_stats["current"] = current

#         # ✅ DRAW UI
#         annotated = draw_ui(annotated, total, current)

#         # ✅ ENCODE FRAME
#         _, buffer = cv2.imencode('.jpg', annotated)
#         frame_bytes = buffer.tobytes()

#         yield (
#             b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
#         )


# # ✅ VIDEO ROUTE
# @app.get("/video")
# def video():
#     return StreamingResponse(
#         generate_frames(),
#         media_type="multipart/x-mixed-replace; boundary=frame"
#     )


# # ✅ STATS API (for dashboard)
# @app.get("/stats")
# def get_stats():
#     return latest_stats

# ... (imports remain the same)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ✅ GLOBAL STATS (Shared between Video and WebSocket)
latest_stats = {"total": 0, "current": 0}

from fastapi import FastAPI
import sqlite3

@app.get("/analytics")
def get_analytics():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%H:%M', timestamp) as time, AVG(current)
        FROM stats
        GROUP BY time
        ORDER BY time
    """)

    data = cursor.fetchall()
    conn.close()

    return {
        "labels": [row[0] for row in data],
        "values": [int(row[1]) for row in data]
    }


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ CLEANER WEBSOCKET: Just sends the global data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send the current global stats to the frontend
            await websocket.send_json(latest_stats)
            # Control the update frequency (e.g., 2 times per second)
            await asyncio.sleep(0.5) 
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

# ✅ VIDEO STREAM FUNCTION (The "Worker")
def generate_frames():
    # Only ONE instance of the camera/tracker/counter exists here
    cam = Camera()
    tracker = PersonTracker()
    counter = PeopleCounter()

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        results = tracker.track(frame)
        annotated = results[0].plot()

        if results[0].boxes is not None and len(results[0].boxes) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else list(range(len(boxes)))
        else:
            boxes, ids = [], []

        # ✅ UPDATE THE SHARED GLOBAL DICTIONARY
        total, current = counter.update(boxes, ids)
        latest_stats["total"] = total
        latest_stats["current"] = current

        annotated = draw_ui(annotated, total, current)
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video")
def video():
    return StreamingResponse(generate_frames(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")