from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path

import streamlit as st
from ultralytics import YOLO

from brevo_alerts import (
    BrevoConfigurationError,
    BrevoSendError,
    send_confirmed_accident_email,
)
from video_processor import process_video

ROOT = Path(__file__).parent
OUTPUT_ROOT = ROOT / "event_snapshots"
MODEL_PATH = ROOT / "accident_best.pt"
if not MODEL_PATH.exists():
    MODEL_PATH = ROOT / "yolov8s.pt"

DEFAULT_SENDER_EMAIL = "abhayajb999@gmail.com"


def parse_email_list(value: str) -> str:
    emails = []
    for item in value.replace(";", ",").split(","):
        cleaned = item.strip()
        if cleaned:
            emails.append(cleaned)
    return ", ".join(emails)


@st.cache_resource
def load_model() -> YOLO:
    return YOLO(str(MODEL_PATH))


st.set_page_config(page_title="AI Traffic Management System", layout="wide")
st.markdown("""
<style>
.stApp { background:#080305; color:white; }
.big-header { background:linear-gradient(135deg,#aa0022,#220005); color:white; text-align:center; padding:25px; border-radius:15px; font-size:36px; font-weight:bold; border:1px solid #ff3355; }
.creator { background:#12070b; color:#ff3355; text-align:center; padding:8px; border-radius:8px; margin-top:10px; }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="big-header">AI-ENABLED INTELLIGENT TRAFFIC MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="creator">OPERATIONAL CONTROL DASHBOARD // DEVELOPED BY: <b>POSSPOLE</b></div>', unsafe_allow_html=True)

st.subheader("Upload Video for Live Analysis")
st.caption("Upload traffic.mp4.mp4 or another supported video. Alerts appear first; snapshots are saved only after accident confirmation.")
video = st.file_uploader("Traffic video", type=["mp4", "avi", "mov", "mkv"])
st.subheader("Processing settings")
settings_col, timing_col = st.columns(2)
with settings_col:
    confidence = st.slider(
        "Detection confidence (0.10-0.80)",
        min_value=0.10,
        max_value=0.80,
        value=0.20,
        step=0.05,
        format="%.2f",
        help="Lower values detect more objects but may include more false detections.",
    )
with timing_col:
    alert_frames = st.number_input(
        "Accident alert delay (frames)",
        min_value=5,
        max_value=300,
        value=15,
        step=5,
        format="%d",
        help="Show an alert after the same tracked vehicle appears stopped for this many frames.",
    )
    confirmation_frames = st.number_input(
        "Accident confirmation delay (frames)",
        min_value=int(alert_frames) + 1,
        max_value=600,
        value=max(45, int(alert_frames) + 1),
        step=5,
        format="%d",
        help="Save an incident image only after this longer stopped period is reached.",
    )
st.caption("The confirmation delay must always be longer than the alert delay.")

st.subheader("Brevo alert contacts")
api_key_col, email_col_1, email_col_2 = st.columns(3)
with api_key_col:
    brevo_api_key = st.text_input(
        "Brevo API key",
        value=os.getenv("BREVO_API_KEY", ""),
        type="password",
        help="Paste your Brevo API key here before running the video analysis.",
    )
with email_col_1:
    sender_email = st.text_input(
        "Sender email",
        value=os.getenv("BREVO_SENDER_EMAIL", DEFAULT_SENDER_EMAIL),
        help="This is your verified Brevo sender address.",
    )
with email_col_2:
    recipient_emails = st.text_input(
        "Recipient email(s)",
        value=os.getenv("BREVO_RECIPIENT_EMAIL", ""),
        placeholder="name@example.com, second@example.com",
        help="Separate multiple recipients with commas.",
    )
st.caption("When an accident is confirmed, the alert is sent through your Brevo API key to the target email addresses above.")

def test_brevo_connection() -> str:
    if not brevo_api_key.strip():
        return "Enter a Brevo API key first."
    if brevo_api_key.strip().startswith("xsmtpsib-"):
        return "This looks like a Brevo SMTP key, not the API key needed for the HTTP v3 endpoint. Generate a Brevo API key under SMTP & API > API Keys."
    if not sender_email.strip():
        return "Enter a verified sender email first."
    try:
        from brevo_alerts import send_confirmed_accident_email
        import tempfile
        from pathlib import Path

        dummy_path = Path(tempfile.gettempdir()) / "brevo_test_check.txt"
        dummy_path.write_text("Brevo connectivity check", encoding="utf-8")
        try:
            send_confirmed_accident_email(
                image_path=dummy_path,
                timestamp_seconds=0,
                frame_number=0,
                sender_email=sender_email,
                recipient_emails=parse_email_list(recipient_emails),
            )
            return "Brevo connection successful."
        finally:
            if dummy_path.exists():
                dummy_path.unlink()
    except Exception as exc:  # pragma: no cover
        return f"Brevo test failed: {exc}"

brevo_test = st.button("Test Brevo connection")
if brevo_test:
    os.environ["BREVO_API_KEY"] = brevo_api_key.strip()
    os.environ["BREVO_SENDER_EMAIL"] = sender_email.strip() or DEFAULT_SENDER_EMAIL
    os.environ["BREVO_RECIPIENT_EMAIL"] = parse_email_list(recipient_emails)
    st.info(test_brevo_connection())

start = st.button("Start video processing", type="primary", disabled=video is None)

if start and video is not None:
    run_dir = OUTPUT_ROOT / f"{Path(video.name).stem}_{int(time.time())}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(video.name).suffix) as temp_file:
        temp_file.write(video.getbuffer())
        video_path = Path(temp_file.name)

    frame_view = st.empty()
    status_view = st.empty()
    progress = st.progress(0, text=f"Loading {MODEL_PATH.name}...")
    metrics = st.columns(8)
    metric_slots = [column.empty() for column in metrics]
    incident_view = st.container()
    try:
        os.environ["BREVO_API_KEY"] = brevo_api_key.strip()
        os.environ["BREVO_SENDER_EMAIL"] = sender_email.strip() or DEFAULT_SENDER_EMAIL
        os.environ["BREVO_RECIPIENT_EMAIL"] = parse_email_list(recipient_emails)

        updates = process_video(video_path, load_model(), run_dir, confidence=float(confidence), alert_frames=int(alert_frames), confirmation_frames=int(confirmation_frames))
        last_update = None
        saved = 0
        for update in updates:
            last_update = update
            frame_view.image(update["frame"], channels="RGB", use_container_width=True)
            total = update["total_frames"]
            progress.progress(min(update["frame_number"] / total, 1.0) if total else 0, text=f"Processing frame {update['frame_number']} of {total or '?'}")
            if update["confirmed_accident"]:
                status_view.error("CONFIRMED ACCIDENT - SNAPSHOT SAVED")
            elif update["accident_alert"]:
                status_view.warning("ACCIDENT ALERT - waiting for confirmation")
            else:
                status_view.info("Monitoring traffic...")
            if update["frame_number"] == 1 or update["frame_number"] % 5 == 0 or not total:
                metric_slots[0].metric("Total", update["vehicles"])
                metric_slots[1].metric("Bicycle", update["counts"]["bicycle"])
                metric_slots[2].metric("Car", update["counts"]["car"])
                metric_slots[3].metric("Motorcycle", update["counts"]["motorcycle"])
                metric_slots[4].metric("Bus", update["counts"]["bus"])
                metric_slots[5].metric("Truck", update["counts"]["truck"])
                metric_slots[6].metric("FPS", update["fps"])
                metric_slots[7].metric("Latency", f"{update['latency']} ms")
            for incident in update["incidents"]:
                saved += 1
                with incident_view:
                    st.error(f"Confirmed accident at {incident.timestamp:.1f}s")
                    st.image(incident.image_path, caption=incident.image_path, use_container_width=True)
                    try:
                        send_confirmed_accident_email(
                            incident.image_path,
                            incident.timestamp,
                            incident.frame,
                            sender_email=sender_email,
                            recipient_emails=parse_email_list(recipient_emails),
                        )
                        st.success("Incident snapshot emailed through Brevo.")
                    except BrevoConfigurationError:
                        st.info(
                            "Brevo email skipped. Set BREVO_API_KEY, "
                            "BREVO_SENDER_EMAIL, and BREVO_RECIPIENT_EMAIL."
                        )
                    except BrevoSendError as error:
                        st.warning(f"Brevo email failed: {error}")
        if last_update is not None:
            counts = last_update["counts"]
            metric_slots[0].metric("Total", last_update["vehicles"])
            metric_slots[1].metric("Bicycle", counts["bicycle"])
            metric_slots[2].metric("Car", counts["car"])
            metric_slots[3].metric("Motorcycle", counts["motorcycle"])
            metric_slots[4].metric("Bus", counts["bus"])
            metric_slots[5].metric("Truck", counts["truck"])
            metric_slots[6].metric("FPS", last_update["fps"])
            metric_slots[7].metric("Latency", f"{last_update['latency']} ms")
        progress.progress(1.0, text="Video processing complete")
        st.success(f"Saved {saved} confirmed incident image(s) in {run_dir}" if saved else "Complete: no confirmed accident snapshot was created.")
    except Exception as error:
        st.error(f"Video processing failed: {error}")
    finally:
        video_path.unlink(missing_ok=True)

st.divider()
st.subheader("Latest Camera Data")
try:
    data = json.loads((ROOT / "traffic_data.json").read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    data = {}
for column, label, key in zip(st.columns(5), ("Cars", "Bicycles", "Motorcycles", "Buses", "Trucks"), ("cars", "bicycles", "motorcycles", "buses", "trucks")):
    column.metric(label, data.get(key, 0))
