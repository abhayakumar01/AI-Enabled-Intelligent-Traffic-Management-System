# 🚦 AI-Enabled Intelligent Traffic Management System (ITMS)

An AI-powered Intelligent Traffic Management System that uses **YOLOv8**, **OpenCV**, and **Streamlit** to monitor traffic, detect vehicles in real-time, analyze traffic density, and optimize traffic signal timing for efficient traffic flow.

---

## 📌 Overview

Traffic congestion is a major challenge in modern cities, leading to delays, fuel wastage, and increased pollution. This project utilizes Artificial Intelligence and Computer Vision to automate traffic monitoring and dynamically control traffic signals based on real-time traffic conditions.

The system detects vehicles using the YOLOv8 object detection model, calculates traffic density, and adjusts traffic signal timing accordingly. It also provides emergency vehicle prioritization to improve response times.

---

## ✨ Features

- 🚗 Real-time Vehicle Detection using YOLOv8
- 📹 Live Video Processing with OpenCV
- 🚦 Intelligent Traffic Signal Control
- 📊 Traffic Density Analysis
- 🚑 Emergency Vehicle Priority System
- 📈 Live Streamlit Dashboard
- ⚡ Automatic Signal Timing Adjustment
- 🖥️ User-Friendly Interface

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| YOLOv8 | Vehicle Detection |
| OpenCV | Video Processing |
| Streamlit | Interactive Dashboard |
| NumPy | Numerical Computation |
| Pandas | Data Handling |

---

## 📂 Project Structure

```text
AI-Enabled-Intelligent-Traffic-Management-System/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── static/
├── src/
├── models/
├── output/
├── videos/
├── images/
└── screenshots/
```

---

## ⚙️ How It Works

1. Capture traffic video or camera feed.
2. Process each frame using OpenCV.
3. Detect vehicles using the YOLOv8 model.
4. Count the detected vehicles.
5. Analyze traffic density.
6. Determine the optimal traffic signal duration.
7. Display live statistics on the Streamlit dashboard.

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/mustafajaved304/AI-Enabled-Intelligent-Traffic-Management-System.git
```

### Move into the Project Folder

```bash
cd AI-Enabled-Intelligent-Traffic-Management-System
```

### Install Required Libraries

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

or

```bash
streamlit run app.py
```

*(Run the command that matches your project structure.)*

---

## 📊 Workflow

```text
Traffic Camera / Video
          │
          ▼
OpenCV Video Processing
          │
          ▼
YOLOv8 Vehicle Detection
          │
          ▼
Vehicle Counting
          │
          ▼
Traffic Density Analysis
          │
          ▼
AI Decision Engine
          │
          ▼
Traffic Signal Timing
          │
          ▼
Live Dashboard
```

---

## 📷 Screenshots

> Add screenshots of your project inside a folder named **screenshots**.

Example:

- Dashboard
- Vehicle Detection
- Traffic Analysis
- Signal Control
- Emergency Vehicle Detection

---

## 🎯 Objectives

- Reduce traffic congestion.
- Improve traffic signal efficiency.
- Detect vehicles accurately in real time.
- Prioritize emergency vehicles.
- Support future smart city applications.

---

## 🔮 Future Enhancements

- 🚁 Drone-Based Traffic Monitoring
- 🚓 Automatic Accident Detection
- 🚘 License Plate Recognition (ANPR)
- ☁️ Cloud-Based Monitoring
- 📱 Mobile Application
- 🗺️ Google Maps Integration
- 🤖 AI-Based Traffic Prediction

---

## 📚 Applications

- Smart Cities
- Traffic Monitoring Centers
- Highways
- Urban Road Networks
- Emergency Response Systems
- Intelligent Transportation Systems (ITS)

---

## 👨‍💻 Author

**Mustafa Mehmood Javed**

BS Cyber Security

GitHub: https://github.com/mustafajaved304

---

## 📄 License

This project is developed for educational and research purposes.

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
