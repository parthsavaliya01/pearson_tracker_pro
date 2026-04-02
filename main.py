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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

latest_stats = {"total": 0, "current": 0, "entered": 0, "exited": 0}

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(latest_stats)
            await asyncio.sleep(0.5) 
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

def generate_frames():
    cam = Camera()
    tracker = PersonTracker()
    counter = PeopleCounter()

    frame_count = 0  
    try:
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

     
            total, current, entered, exited = counter.update(boxes, ids)

           
            latest_stats["total"] = total
            latest_stats["current"] = current
            latest_stats["entered"] = entered
            latest_stats["exited"] = exited

  
            frame_count += 1
            if frame_count % 10 == 0:
                insert_stats(total, current)

            
            annotated = draw_ui(annotated, total, current, entered, exited)

            _, buffer = cv2.imencode('.jpg', annotated)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        cam.release()  


@app.get("/video")
def video():
    return StreamingResponse(generate_frames(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")