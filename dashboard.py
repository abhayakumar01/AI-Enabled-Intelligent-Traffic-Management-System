import streamlit as st
import time
import json

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="AI Traffic Management System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================
# CSS THEME
# ==================================
st.markdown("""
<style>

.stApp {
    background-color: #080305;
    color: white;
}

.big-header {
    background: linear-gradient(135deg, #aa0022 0%, #220005 100%);
    color: white;
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    font-size: 36px;
    font-weight: bold;
    border: 1px solid #ff3355;
}

.creator {
    background: #12070b;
    color: #ff3355;
    text-align: center;
    padding: 8px;
    border-radius: 8px;
    margin-top: 10px;
}

.crypto-card {
    background: rgba(24,17,19,0.7);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #333;
}

.card-label {
    font-size: 14px;
    color: #cccccc;
}

.card-value {
    font-size: 32px;
    font-weight: bold;
    color: #ff3355;
}

.traffic-hud {
    background: #111;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    margin-top: 15px;
}

.status-box {
    background: #12070b;
    color: white;
    text-align: center;
    padding: 18px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    border-left: 6px solid #ff3355;
}

.green {
    color: #00ff66;
}

.red {
    color: #ff3333;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# HEADER
# ==================================
st.markdown("""
<div class="big-header">
🚦 AI-ENABLED INTELLIGENT TRAFFIC MANAGEMENT SYSTEM
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="creator">
OPERATIONAL CONTROL DASHBOARD // DEVELOPED BY: <b>MUSTAFA MEHMOOD JAVED</b>
</div>
""", unsafe_allow_html=True)

placeholder = st.empty()

while True:

    with placeholder.container():

        # ==================================
        # LOAD LIVE DATA
        # ==================================
        try:

            with open("traffic_data.json", "r") as f:
                live = json.load(f)

            cars = live.get("cars", 0)
            buses = live.get("buses", 0)
            trucks = live.get("trucks", 0)
            bikes = live.get("motorcycles", 0)

            total = live.get("total", 0)

            status = live.get("status", "LOW")
            latency = live.get("latency", 0)
            fps = live.get("fps", 0)

            emergency = live.get("emergency", False)
            accident = live.get("accident", False)

        except:

            cars = 0
            buses = 0
            trucks = 0
            bikes = 0

            total = 0

            status = "WAITING"
            latency = 0
            fps = 0

            emergency = False
            accident = False

        # ==================================
        # SIGNAL LOGIC
        # ==================================
        if emergency:
            signal = "GREEN"
        elif status == "LOW":
            signal = "GREEN"
        else:
            signal = "RED"

        score = min(total * 10, 100)

        # ==================================
        # VEHICLE CARDS
        # ==================================
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f'<div class="crypto-card"><div class="card-label">🚗 Cars</div><div class="card-value">{cars}</div></div>',
                unsafe_allow_html=True)

        with c2:
            st.markdown(
                f'<div class="crypto-card"><div class="card-label">🚌 Buses</div><div class="card-value">{buses}</div></div>',
                unsafe_allow_html=True)

        with c3:
            st.markdown(
                f'<div class="crypto-card"><div class="card-label">🚚 Trucks</div><div class="card-value">{trucks}</div></div>',
                unsafe_allow_html=True)

        with c4:
            st.markdown(
                f'<div class="crypto-card"><div class="card-label">📊 Total Vehicles</div><div class="card-value">{total}</div></div>',
                unsafe_allow_html=True)

        st.write("")

        # ==================================
        # SIGNAL DISPLAY
        # ==================================
        signal_color = "green" if signal == "GREEN" else "red"

        st.markdown(f"""
        <div class="traffic-hud">
            <h2 class="{signal_color}">
            🚦 SIGNAL STATUS : {signal}
            </h2>
        </div>
        """, unsafe_allow_html=True)

        # ==================================
        # STATUS BOX
        # ==================================
        st.markdown(f"""
        <div class="status-box">
        🤖 Traffic Condition : {status}
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ==================================
        # METRICS
        # ==================================
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric("📈 Congestion Score", f"{score}")

        with m2:
            st.metric("⚡ Latency (ms)", f"{latency}")

        with m3:
            st.metric("🎥 FPS", f"{fps}")

        with m4:
            st.metric("🏍️ Motorcycles", f"{bikes}")

        st.markdown("---")

        # ==================================
        # DENSITY BARS
        # ==================================
        st.subheader("📊 Real-Time Vehicle Density")

        st.progress(min(cars / 50, 1.0),
                    text=f"🚗 Cars : {cars}")

        st.progress(min(buses / 20, 1.0),
                    text=f"🚌 Buses : {buses}")

        st.progress(min(trucks / 20, 1.0),
                    text=f"🚚 Trucks : {trucks}")

        st.progress(min(bikes / 30, 1.0),
                    text=f"🏍️ Motorcycles : {bikes}")

        st.markdown("---")

        # ==================================
        # TELEMETRY
        # ==================================
        st.subheader("📡 System Telemetry")

        st.success("🤖 YOLOv8 Detection Engine Active")
        st.success("📹 Live Camera Feed Connected")

        if emergency:
            st.error("🚑 Emergency Vehicle Priority Activated")

        if accident:
            st.warning("⚠️ Accident Alert Triggered")

        st.info("🎯 Model: YOLOv8 Nano")

        st.markdown("""
        <center>
        <br>
        <span style="color:#888;">
        AI TRAFFIC MANAGEMENT SYSTEM • CCP PROJECT • 2026
        </span>
        </center>
        """, unsafe_allow_html=True)

    time.sleep(1)