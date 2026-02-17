import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import glob
import cv2

st.set_page_config(
    page_title="SkyGuard AI - Ground Control Station",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stMetric {
        color: #00FF00 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛸 SkyGuard AI - Mission Control")

# Sidebar
with st.sidebar:
    st.header("System Status")
    connection_status = st.empty()
    connection_status.success("Connected to Telemetry Stream")
    
    st.divider()
    
    st.subheader("Mission Control")
    if st.button("ARM SYSTEM", type="primary"):
        st.toast("System ARMED!", icon="⚠️")
    
    if st.button("RETURN TO LAUNCH"):
        st.toast("RTL Mode Activated", icon="🏠")
        
    if st.button("EMERGENCY STOP", type="primary"):
        st.error("EMERGENCY STOP ACTIVATED")

# Layout
col1, col2 = st.columns([2, 1])

# Mock Data Generator
def get_mock_data():
    return {
        "roll": np.random.normal(0, 2),
        "pitch": np.random.normal(0, 2),
        "yaw": np.random.normal(0, 180),
        "altitude": np.random.normal(10, 0.5),
        "battery": 95 - (time.time() % 100) / 10,
        "speed": np.random.normal(5, 1)
    }

# Main Dashboard
with col1:
    st.subheader("Live Video Feed (Simulated)")
    # Placeholder for video stream
    video_placeholder = st.empty()
    
    # Simulate video feed
    # In real app, this would pull from a camera stream or websocket
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "NO SIGNAL", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    video_placeholder.image(img, channels="BGR", use_column_width=True)

with col2:
    st.subheader("Telemetry")
    
    # Live metrics
    data = get_mock_data()
    
    m1, m2 = st.columns(2)
    m1.metric("Altitude", f"{data['altitude']:.1f} m", "0.1 m")
    m2.metric("Ground Speed", f"{data['speed']:.1f} m/s", "-0.2 m/s")
    
    m3, m4 = st.columns(2)
    m3.metric("Battery", f"{data['battery']:.1f} %", "-0.1 %")
    m4.metric("Link Quality", "98 %", "0 %")
    
    st.divider()
    
    st.subheader("Attitude")
    st.write(f"**Roll:** {data['roll']:.2f}°")
    st.progress((data['roll'] + 30) / 60)
    
    st.write(f"**Pitch:** {data['pitch']:.2f}°")
    st.progress((data['pitch'] + 30) / 60)

# Charts
st.subheader("Flight History")
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['time', 'altitude'])

new_row = pd.DataFrame({'time': [time.time()], 'altitude': [data['altitude']]})
st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(100)

st.line_chart(st.session_state.history.set_index('time'))

# Auto-refresh
time.sleep(1)
st.rerun()
