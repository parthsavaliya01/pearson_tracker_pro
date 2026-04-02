# 🚀 AI Employee Monitoring System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

---

## 🎥 Demo

> ⚠️ Add your demo GIF here (very important for recruiters)


---

## 📸 Screenshots

### Dashboard
![Dashboard](assets/dashboard.png)

### Detection + Tracking
![Tracking](assets/tracking.png)

---

## 📌 Overview

A **real-time computer vision system** for detecting, tracking, and analyzing employee movement using live video streams.

The system provides:
- Live occupancy monitoring  
- Entry/Exit analytics via door  
- Real-time dashboard with analytics  

---

## ✨ Features

- 🎯 YOLOv8-based real-time person detection  
- 🧠 ByteTrack multi-object tracking (unique IDs)  
- 🔢 Live + Total people counting  
- 🚪 Entry/Exit detection using door line-crossing  
- 📊 Live dashboard (FastAPI + WebSocket)  
- 📈 Analytics graph (Chart.js)  
- 🗄️ SQLite database logging  
- ⚡ RTSP/Webcam support  
- 🐳 Docker deployment ready  

---

## 🧠 System Architecture
Camera → YOLOv8 → ByteTrack → Counter Logic → FastAPI
↓
WebSocket + DB
↓
Frontend UI


---

## 🛠️ Tech Stack

- **CV**: YOLOv8, OpenCV  
- **Tracking**: ByteTrack  
- **Backend**: FastAPI  
- **Frontend**: HTML, JS, Chart.js  
- **Database**: SQLite  
- **Deployment**: Docker  

---

## ⚙️ Setup

### 1. Clone

git clone https://github.com/your-username/employee-tracker-pro.git

cd employee-tracker-pro


### 2. Install

pip install -r requirements.txt


### 3. Run

uvicorn main:app --reload


👉 Open: http://127.0.0.1:8000

---

## 🐳 Docker


docker build -t employee-tracker .
docker run -p 8000:8000 employee-tracker


---

## 🚪 Entry / Exit Logic

- Virtual line placed at door  
- Left → Right → ENTRY  
- Right → Left → EXIT  

### Stability Improvements:
- Buffer zone (OFFSET)  
- Minimum movement threshold  
- ID consistency tracking  

---

## 📊 API

| Endpoint     | Description        |
|-------------|-------------------|
| `/`         | Dashboard         |
| `/video`    | Live stream       |
| `/ws`       | Live stats        |
| `/analytics`| Historical data   |

---

## 📁 Structure


src/
├── camera.py
├── tracker.py
├── counter.py
└── utils.py

templates/
└── index.html

main.py
config.py
db.py
Dockerfile


---

## 🚀 Highlights

- Real-time low-latency system  
- Entry/Exit intelligence (not just counting)  
- Full-stack CV + Backend + UI  
- Deployment-ready  

---

## ⚠️ Challenges

- ID switching  
- False line crossing  
- RTSP latency  

---

## ✅ Solutions

- Distance-based ID mapping  
- Buffer + movement filtering  
- Frame skipping optimization  

---

## 🔮 Future Work

- Heatmaps  
- Zone detection  
- Alerts system  
- Cloud deployment  

---

## 👨‍💻 Author

**Parth Savaliya**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!