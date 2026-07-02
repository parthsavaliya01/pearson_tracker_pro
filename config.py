import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "yolov8n.pt"))
VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", "0")
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "640"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "480"))
LINE_POSITION = int(os.getenv("LINE_POSITION", "310"))
INSIDE_DIRECTION = os.getenv("INSIDE_DIRECTION", "right").lower()
EDGE_MARGIN = int(os.getenv("EDGE_MARGIN", "60"))
DETECTION_CONFIDENCE = float(os.getenv("DETECTION_CONFIDENCE", "0.45"))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", "0.50"))
TRACKER_CONFIDENCE = float(os.getenv("TRACKER_CONFIDENCE", "0.45"))
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "tracker.db"))
DATA_DIR = BASE_DIR / "data"
