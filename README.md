# Employee Tracker PRO

A production-ready real-time employee tracking system built with Python, FastAPI, YOLOv8, and OpenCV. The project detects people, tracks them with stable IDs, counts entries and exits across a configurable virtual door line, and serves a live dashboard with analytics and streaming video.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)![![Production--Ready-brightgreen)


---

## Features

- Real-time person detection using YOLOv8
- Multi-object tracking with stable tracking IDs
- Entry/exit counting for door-crossing events
- Live occupancy monitoring
- Web-based dashboard with live updates
- Analytics charting and historical logging
- SQLite persistence for stats
- Webcam-first operation with graceful camera fallback
- Docker-ready deployment

---

## Tech Stack

- Python 3.12
- FastAPI
- Jinja2 Templates
- OpenCV
- YOLOv8
- NumPy
- SQLite
- Docker
- pytest

---

## Project Structure

```text
employee_tracker_pro/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration values and environment defaults
├── db.py                   # SQLite database helpers
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose setup
├── .env.example            # Sample environment file
├── templates/              # HTML dashboard templates
├── static/                 # Static assets
├── src/
│   ├── camera.py           # Camera access and fallback logic
│   ├── counter.py          # Entry/exit counting logic
│   ├── tracker.py          # Person detection and tracking
│   └── utils.py            # UI drawing helpers
├── tests/                  # Unit tests
├── models/                 # YOLO model file
└── data/                   # Database and runtime data
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd employee_tracker_pro
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the YOLO model

The project expects the model file at:

```text
models/yolov8n.pt
```

If the file is missing, place the YOLOv8 nano model there before running the app.

---

## Configuration

Copy the sample environment file and adjust values as needed:

```bash
cp .env.example .env
```

### Main configuration options

- `VIDEO_SOURCE`: camera device index or stream URL
- `FRAME_WIDTH`: width of the processed frame
- `FRAME_HEIGHT`: height of the processed frame
- `LINE_POSITION`: x-coordinate of the counting line
- `INSIDE_DIRECTION`: direction that represents entry
- `EDGE_MARGIN`: margin used for confirmation logic
- `DETECTION_CONFIDENCE`: model confidence threshold
- `IOU_THRESHOLD`: non-maximum suppression threshold
- `DB_PATH`: path to the SQLite database
- `MODEL_PATH`: model file path

---

## Run Locally

Start the FastAPI app:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

### Useful run options

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

If port 8000 is already in use, try another port:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

## API Endpoints

- `GET /` — Dashboard page
- `GET /video` — Live video stream
- `GET /analytics` — Analytics data
- `GET /health` — Health check
- `GET /ws` — WebSocket updates for live stats

---

## Database

The application uses SQLite to store analytics records such as:

- total count
- current occupancy
- entries
- exits
- timestamp

The database is created automatically when the app starts.

---

## Docker Usage

### Build the image

```bash
docker build -t employee-tracker .
```

### Run the container

```bash
docker run -p 8000:8000 employee-tracker
```

### Docker Compose

```bash
docker compose up --build
```

---

## Testing

Run the test suite:

```bash
pytest -q
```

Current tests cover the core entry/exit counting logic.

---

## Troubleshooting

### Port already in use
If you see an address already in use error, stop the existing process or run the app on another port.

### Camera not found
If the webcam cannot be opened, the app will show a graceful error state instead of crashing.

### Model file missing
Ensure the YOLO model exists at `models/yolov8n.pt`.

---



## Future Improvements

- Better occupancy analytics and charts
- Zone-based monitoring
- Alerting and notifications
- Cloud deployment support
- Improved tracking robustness for crowded environments

---

## License

This project is licensed under the MIT License.
