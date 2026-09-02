# AI-Enabled Intelligent Traffic Management System

A computer vision and AI-based traffic monitoring project designed to detect vehicles, monitor traffic density, detect potential accidents, and prioritize emergency vehicles. The system uses YOLOv8, OpenCV, and Streamlit to process video and present a live dashboard for traffic control and incident monitoring.

---

## 1. Project Overview

This project helps automate traffic management by analyzing road footage and identifying key conditions such as:

- vehicle counts by type
- traffic density level
- accident or stopped-vehicle warning
- emergency vehicle detection
- snapshot saving for confirmed incidents
- Brevo email notifications for confirmed accident alerts

The app is built as a dashboard-driven system that can process uploaded traffic video and visualize the detected results in real time.

---

## 2. Features

- Real-time vehicle detection using YOLOv8
- Traffic density estimation
- Accident alert and confirmation logic
- Emergency vehicle priority detection
- Streamlit-based monitoring dashboard
- Incident snapshot saving to the event_snapshots folder
- Optional email notifications through Brevo
- Model fallback to YOLOv8 base weights if custom accident model is not available

---

## 3. Technologies Used

- Python 3.10+
- OpenCV
- Ultralytics YOLOv8
- Streamlit
- NumPy
- Pandas
- TensorFlow / PyTorch dependency stack via YOLOv8
- Brevo API for sending email alerts

---

## 4. Project Structure

```text
AI-Enabled-Intelligent-Traffic-Management-System/
├── README.md
├── requirements.txt
├── main.py
├── dashboard.py
├── detector.py
├── emergency.py
├── signal_control.py
├── accident.py
├── prediction.py
├── utils.py
├── shared_data.py
├── video_processor.py
├── brevo_alerts.py
├── train_accident_model.py
├── accident_dataset.yaml
├── traffic_data.json
├── traffic.mp4.mp4
├── yolov8n.pt
├── yolov8s.pt
├── accident_best.pt   # optional custom trained model
├── event_snapshots/
├── tests/
├── video_runs/
└── .git/
```

---

## 5. Requirements

Before setup, make sure your computer has:

- Python 3.10 or newer
- pip installed
- Git installed
- A working GPU is optional, but CPU works for basic testing
- An internet connection to install dependencies

---

## 6. Setup Instructions on a New Computer

### Step 1: Clone the project

```bash
git clone https://github.com/your-username/AI-Enabled-Intelligent-Traffic-Management-System.git
cd AI-Enabled-Intelligent-Traffic-Management-System
```

If you already have the project folder locally, skip the clone step and move to the next one.

### Step 2: Create a virtual environment

On Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If installation fails on a specific machine, you can install the key packages manually:

```bash
pip install ultralytics opencv-python numpy pandas streamlit matplotlib torch tensorflow
```

### Step 4: Confirm the project runs

From the project root:

```bash
python -m streamlit run dashboard.py
```

The dashboard should open in your browser at:

```text
http://localhost:8501
```

If the app is already configured locally, it may also be launched from a terminal with:

```bash
streamlit run dashboard.py
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

## 10. How the System Works

```text
Video input
    ↓
OpenCV frame extraction
    ↓
YOLOv8 object detection
    ↓
Vehicle counting and classification
    ↓
Traffic density analysis
    ↓
Emergency vehicle check
    ↓
Accident alert and confirmation logic
    ↓
Snapshot saving + optional Brevo email
    ↓
Streamlit dashboard reporting
```

---

## 11. Troubleshooting

### Streamlit does not open

- Make sure the virtual environment is activated.
- Reinstall dependencies: `pip install -r requirements.txt`
- Use `python -m streamlit run dashboard.py` instead of `streamlit run` if needed.

### Model errors

- Ensure that `yolov8n.pt` or `yolov8s.pt` is present in the project root.
- If a custom accident model is missing, the app will fall back to the default YOLO model.

### Video does not process

- Check that your uploaded video file is valid.
- Confirm the file extension is supported.
- Ensure OpenCV can read the video in your environment.

### Brevo email fails

- Check the API key.
- Make sure the sender email is verified in Brevo.
- Ensure the recipient email is valid.
- Verify that the environment variables are set before starting the app.

---

## 12. Deployment Notes

This project is designed for local testing and monitoring. For a real deployment, you may later add:

- a web server deployment setup
- persistent storage for snapshots
- production-ready database logging
- alert management and dashboard authentication
- a dedicated camera streaming source instead of uploaded video

---

## 13. Project Goals

This project is useful for:

- smart city traffic monitoring
- intelligent transportation systems
- road safety analysis
- emergency vehicle prioritization
- AI-based traffic signal decision support

---

## 14. License

This project is intended for educational, research, and demonstration purposes.

---

## 15. Author / Credits

Project developed for AI-driven intelligent transportation and traffic monitoring research.

---

## 16. Quick Start Summary

```bash
git clone <repo-url>
cd AI-Enabled-Intelligent-Traffic-Management-System
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
# source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run dashboard.py
```

Open the app in your browser at:

```text
http://localhost:8501
```

This is the simplest way to install and run the project on another computer.
