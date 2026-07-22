import streamlit as st
import time
from shared_data import data

st.title("🚦 REAL TIME ITMS DASHBOARD")

placeholder = st.empty()

while True:
    with placeholder.container():

        st.metric("Cars", data["cars"])
        st.metric("Buses", data["buses"])
        st.metric("Trucks", data["trucks"])

        st.metric("Traffic Score", data["score"])
        st.metric("Green Signal Time", f'{data["signal"]} sec')

        st.write("Status:", data["status"])
        st.write("Latency:", f'{data["latency"]} ms')

    time.sleep(1)