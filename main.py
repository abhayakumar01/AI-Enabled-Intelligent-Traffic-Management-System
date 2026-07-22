import cv2
import time
import json
from ultralytics import YOLO

# =========================
# INIT
# =========================
model = YOLO("yolov8n.pt")

# Camera
cap = cv2.VideoCapture(0)

prev_time = time.time()
prev_total = 0
stuck_frames = 0

print("🚦 AI Traffic Management System Running...")

# =========================
# MAIN LOOP
# =========================
while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Camera Frame Error")
        break

    frame = cv2.resize(frame, (800, 450))

    start_time = time.time()

    # =========================
    # YOLO DETECTION
    # =========================
    results = model(frame, verbose=False)

    annotated = results[0].plot()

    cars = 0
    buses = 0
    trucks = 0
    motorcycles = 0

    emergency = False

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "car":
                cars += 1

            elif label == "bus":
                buses += 1

            elif label == "truck":
                trucks += 1

            elif label == "motorcycle":
                motorcycles += 1

            # Emergency Detection Placeholder
            if label in ["ambulance", "police"]:
                emergency = True

    # =========================
    # TOTAL VEHICLES
    # =========================
    total = cars + buses + trucks + motorcycles

    # =========================
    # ACCIDENT DETECTION
    # =========================
    if total == prev_total:
        stuck_frames += 1
    else:
        stuck_frames = 0

    accident = stuck_frames > 15

    prev_total = total

    # =========================
    # SIGNAL CONTROL
    # =========================
    if emergency:
        signal_time = 90
        status = "EMERGENCY PRIORITY"

    elif accident:
        signal_time = 10
        status = "ACCIDENT ALERT"

    else:

        if total <= 5:
            signal_time = 15
            status = "LOW"

        elif total <= 15:
            signal_time = 30
            status = "MEDIUM"

        else:
            signal_time = 60
            status = "HIGH"

    # =========================
    # PERFORMANCE
    # =========================
    latency = (time.time() - start_time) * 1000

    current_time = time.time()
    fps = 1 / (current_time - prev_time + 0.0001)

    # =========================
    # SAVE DATA FOR DASHBOARD
    # =========================
    dashboard_data = {

        "cars": cars,
        "buses": buses,
        "trucks": trucks,
        "motorcycles": motorcycles,

        "total": total,

        "status": status,
        "signal_time": signal_time,

        "latency": round(latency, 2),
        "fps": round(fps, 2),

        "emergency": emergency,
        "accident": accident
    }

    with open("traffic_data.json", "w") as file:
        json.dump(dashboard_data, file)

    # =========================
    # CONSOLE OUTPUT
    # =========================
    print(
        f"Cars:{cars} | Buses:{buses} | Trucks:{trucks} | "
        f"Motorcycles:{motorcycles} | Total:{total}"
    )

    # =========================
    # DISPLAY INFO
    # =========================
    cv2.putText(
        annotated,
        f"Cars: {cars}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated,
        f"Status: {status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        annotated,
        f"Signal Time: {signal_time}s",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2
    )

    cv2.putText(
        annotated,
        f"FPS: {round(fps,2)}",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    if emergency:
        cv2.putText(
            annotated,
            "EMERGENCY VEHICLE!",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            3
        )

    if accident:
        cv2.putText(
            annotated,
            "ACCIDENT ALERT!",
            (20, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            3
        )

    cv2.imshow("🚦 AI Traffic Management System", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv2.destroyAllWindows()