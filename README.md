# 🚦 AI-Enabled Intelligent Traffic Management System (ITMS)

An AI-powered Intelligent Traffic Management System that utilizes **YOLOv8**, **OpenCV**, and **Streamlit** to monitor traffic, detect vehicles in real time, analyze traffic density, and optimize traffic signal timing for efficient and intelligent traffic management.

---

## 📖 Overview

Traffic congestion has become one of the biggest challenges in modern cities, causing delays, fuel consumption, and environmental pollution. This project applies Artificial Intelligence and Computer Vision to automate traffic monitoring and dynamically manage traffic signals based on real-time vehicle density.

Using the YOLOv8 object detection model, the system detects and counts vehicles from live video feeds, analyzes traffic conditions, and automatically adjusts signal timing to improve traffic flow. The project also includes emergency vehicle prioritization for faster emergency response.

---

## ✨ Key Features

- 🚗 Real-Time Vehicle Detection using YOLOv8
- 📹 Live Traffic Video Processing
- 🚦 Intelligent Traffic Signal Control
- 📊 Traffic Density Analysis
- 🚑 Emergency Vehicle Priority Detection
- 📈 Interactive Streamlit Dashboard
- ⚡ Automatic Signal Timing Optimization
- 🖥️ Real-Time Monitoring Interface

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application Development |
| YOLOv8 | Vehicle Detection |
| OpenCV | Image & Video Processing |
| Streamlit | Dashboard Interface |
| NumPy | Numerical Processing |
| Pandas | Data Processing |

---

## 📂 Project Structure

```text
AI-Enabled-Intelligent-Traffic-Management-System/
│
├── app.py
├── main.py
├── requirements.txt
├── models/
├── src/
├── output/
├── videos/
├── images/
├── README.md
└── .gitignore
```

---

## ⚙️ System Workflow

```text
Traffic Camera / Video
          │
          ▼
OpenCV Frame Processing
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
Signal Timing Decision
          │
          ▼
Emergency Vehicle Detection
          │
          ▼
Traffic Signal Optimization
          │
          ▼
Live Streamlit Dashboard
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/mustafajaved304/AI-Enabled-Intelligent-Traffic-Management-System.git
```

Navigate to the project directory:

```bash
cd AI-Enabled-Intelligent-Traffic-Management-System
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 7. Running the Application

### Launch dashboard

```bash
python -m streamlit run dashboard.py
```

### Upload a video

1. Open the dashboard in the browser.
2. Upload a video file such as mp4, avi, mov, or mkv.
3. Adjust confidence and accident alert timing settings.
4. Click Start video processing.

The app will:

- detect vehicles in frames
- estimate traffic conditions
- show accident alerts
- save incident snapshots when confirmed
- optionally send emails via Brevo

---

## 8. Optional: Brevo Email Alerts

To enable email notifications for confirmed accident incidents, set environment variables before starting the dashboard.

### Windows PowerShell

```powershell
$env:BREVO_API_KEY = "your-api-key"
$env:BREVO_SENDER_EMAIL = "verified-sender@example.com"
$env:BREVO_RECIPIENT_EMAIL = "recipient@example.com"
$env:BREVO_SENDER_NAME = "AI Traffic Management System"
python -m streamlit run dashboard.py
```

### macOS/Linux

```bash
export BREVO_API_KEY="your-api-key"
export BREVO_SENDER_EMAIL="verified-sender@example.com"
export BREVO_RECIPIENT_EMAIL="recipient@example.com"
export BREVO_SENDER_NAME="AI Traffic Management System"
python -m streamlit run dashboard.py
```

Important notes:

- The sender email must be verified in Brevo.
- Use the Brevo API key, not the SMTP key.
- The API key should be kept in environment variables and not committed to the repository.

---

## 9. Accident Model Training

The project supports a custom accident-detection model. If a trained model is not present, the dashboard falls back to the default YOLOv8 weights.

### Recommended dataset structure

```text
datasets/accident/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

### Train the model

```bash
python train_accident_model.py --epochs 100 --imgsz 960 --batch 8
```

If your dataset is stored somewhere else:

```bash
python train_accident_model.py --dataset-root "C:\path\to\datasets\accident" --epochs 100 --imgsz 960 --batch 8
```

After training, place the best model into the project root as:

```text
accident_best.pt
```

The dashboard will use this custom model automatically when it exists.

---

## 🌍 Applications

- Smart City Infrastructure
- Urban Traffic Monitoring
- Highway Traffic Control
- Intelligent Transportation Systems (ITS)
- Emergency Response Management
- Traffic Research and Analytics

---

## 📚 Learning Outcomes

This project demonstrates the practical implementation of Artificial Intelligence, Computer Vision, and intelligent decision-making for traffic management. It combines deep learning with real-time image processing to automate traffic analysis and optimize signal control using modern AI techniques.

---

## 👨‍💻 Author

**Mustafa Mehmood Javed**
GitHub: https://github.com/mustafajaved304

---

## 📄 License

This project is developed for educational and academic purposes.

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
