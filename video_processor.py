from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator

import cv2
from ultralytics import YOLO

VEHICLE_LABELS = ("bicycle", "car", "motorcycle", "bus", "truck", "bike", "van")


@dataclass
class Incident:
    frame: int
    timestamp: float
    image_path: str
    track_id: int


def process_video(video_path: str | Path, model: YOLO, output_dir: str | Path, confidence: float = 0.2, image_size: int = 960, alert_frames: int = 15, confirmation_frames: int = 45) -> Iterator[dict]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError("Could not open the uploaded video.")

    fps_source = capture.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    previous_centers: dict[int, tuple[int, int]] = {}
    stopped: dict[int, int] = {}
    confirmed: set[int] = set()
    incidents: list[Incident] = []
    previous_time = time.perf_counter()
    frame_number = 0
    accident_streak = 0
    custom_accident_saved = False
    model_names = set(model.names.values()) if isinstance(model.names, dict) else set(model.names)
    class_filter = None if "accident" in model_names else [1, 2, 3, 5, 7]

    try:
        while True:
            success, frame = capture.read()
            if not success:
                break
            frame_number += 1
            started = time.perf_counter()
            result = model.track(frame, persist=True, conf=confidence, imgsz=image_size, classes=class_filter, verbose=False)[0]
            annotated = result.plot()
            counts = {label: 0 for label in VEHICLE_LABELS}
            detected_accident = False
            for class_id in result.boxes.cls.int().cpu().tolist():
                label = model.names[int(class_id)]
                if label == "accident":
                    detected_accident = True
                if label in counts:
                    counts[label] += 1

            accident_streak = accident_streak + 1 if detected_accident else 0
            if not detected_accident:
                custom_accident_saved = False

            current_centers: dict[int, tuple[int, int]] = {}
            alert_ids: set[int] = set()
            confirmed_ids: set[int] = set()
            if result.boxes.id is not None:
                ids = result.boxes.id.int().cpu().tolist()
                boxes = result.boxes.xyxy.int().cpu().tolist()
                labels = result.boxes.cls.int().cpu().tolist()
                for track_id, box, class_id in zip(ids, boxes, labels):
                    if model.names[int(class_id)] not in counts:
                        continue
                    left, top, right, bottom = box
                    center = ((left + right) // 2, (top + bottom) // 2)
                    current_centers[track_id] = center
                    previous = previous_centers.get(track_id)
                    if previous is None:
                        continue
                    movement = abs(center[0] - previous[0]) + abs(center[1] - previous[1])
                    stopped[track_id] = stopped.get(track_id, 0) + 1 if movement <= 4 else 0
                    if stopped[track_id] >= alert_frames:
                        alert_ids.add(track_id)
                    if stopped[track_id] >= confirmation_frames:
                        confirmed_ids.add(track_id)

            accident_alert = bool(alert_ids) or accident_streak >= alert_frames
            confirmed_accident = bool(confirmed_ids) or accident_streak >= confirmation_frames

            timestamp = frame_number / fps_source
            new_incidents: list[Incident] = []
            for track_id in confirmed_ids - confirmed:
                confirmed.add(track_id)
                cv2.putText(annotated, "CONFIRMED ACCIDENT - SNAPSHOT SAVED", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                image_path = output / f"confirmed_accident_{frame_number}_{track_id}.jpg"
                cv2.imwrite(str(image_path), annotated)
                incident = Incident(frame_number, timestamp, str(image_path), track_id)
                incidents.append(incident)
                new_incidents.append(incident)

            if accident_streak >= confirmation_frames and not custom_accident_saved:
                custom_accident_saved = True
                cv2.putText(annotated, "CONFIRMED ACCIDENT - SNAPSHOT SAVED", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                image_path = output / f"confirmed_accident_{frame_number}_detector.jpg"
                cv2.imwrite(str(image_path), annotated)
                incident = Incident(frame_number, timestamp, str(image_path), -1)
                incidents.append(incident)
                new_incidents.append(incident)

            previous_centers = current_centers
            now = time.perf_counter()
            elapsed = now - previous_time
            previous_time = now
            yield {
                "frame": cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                "frame_number": frame_number,
                "total_frames": total_frames,
                "vehicles": sum(counts.values()),
                "counts": counts,
                "fps": round(1 / elapsed, 2) if elapsed else 0,
                "latency": round((time.perf_counter() - started) * 1000, 2),
                "accident_alert": accident_alert,
                "confirmed_accident": confirmed_accident,
                "incidents": new_incidents,
            }
    finally:
        capture.release()
        (output / "incidents.json").write_text(json.dumps([asdict(item) for item in incidents], indent=2), encoding="utf-8")
