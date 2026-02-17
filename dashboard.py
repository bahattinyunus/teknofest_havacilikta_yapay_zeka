import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import glob
import cv2
from src.simulation.video_stream import VideoSynthesizer

st.set_page_config(
    page_title="SkyGuard AI - Yer Kontrol İstasyonu",
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

st.title("🛸 SkyGuard AI - Görev Kontrol Merkezi")

# Sidebar
with st.sidebar:
    st.header("Sistem Durumu")
    connection_status = st.empty()
    connection_status.success("Telemetri Akışına Bağlandı")
    
    st.divider()
    
    st.subheader("Görev Kontrolü")
    if st.button("SİSTEMİ BAŞLAT (ARM)", type="primary"):
        st.toast("Sistem BAŞLATILDI (ARMED)!", icon="⚠️")
    
    if st.button("EVE DÖN (RTL)"):
        st.toast("Eve Dönüş Modu Aktif", icon="🏠")
        
    if st.button("ACİL DURDURMA", type="primary"):
        st.error("ACİL DURDURMA AKTİVE EDİLDİ")

    st.divider()
    st.info("Simülasyon Modu Aktif")

# Layout
col1, col2 = st.columns([2, 1])

# Mock Data Generator
def get_mock_data():
    return {
        "roll": np.sin(time.time()) * 5,   # Simulate gentle rolling
        "pitch": np.cos(time.time() * 0.5) * 3, # Simulate gentle pitching
        "yaw": (time.time() * 5) % 360,
        "altitude": 10 + np.sin(time.time() * 0.2) * 2,
        "battery": max(0, 95 - (time.time() % 300) / 3),
        "speed": 5 + np.random.normal(0, 0.5)
    }

# Initialize Simulation
if 'video_sim' not in st.session_state:
    st.session_state.video_sim = VideoSynthesizer()

# Live Data
data = get_mock_data()

# Main Dashboard
with col1:
    st.subheader("Canlı Video Akışı (Yapay Zeka Destekli)")
    # Placeholder for video stream
    video_placeholder = st.empty()
    detections_placeholder = st.empty()
    
    # Generate Frame
    frame, detections = st.session_state.video_sim.generate_frame(data['roll'], data['pitch'])
    
    # Check for targets
    if detections:
        cnt = len(detections)
        detections_placeholder.warning(f"⚠️ {cnt} Hedef Tespit Edildi!")
    else:
        detections_placeholder.success("Alan Temiz")

    video_placeholder.image(frame, channels="BGR", use_column_width=True)

with col2:
    st.subheader("Telemetri")
    
    m1, m2 = st.columns(2)
    m1.metric("İrtifa", f"{data['altitude']:.1f} m", "0.1 m")
    m2.metric("Yer Hızı", f"{data['speed']:.1f} m/s", "-0.2 m/s")
    
    m3, m4 = st.columns(2)
    m3.metric("Pil", f"{data['battery']:.1f} %", "-0.1 %")
    m4.metric("Bağlantı Kalitesi", "98 %", "0 %")
    
    st.divider()
    
    st.subheader("Yönelim (Attitude)")
    
    # Roll Gauge
    st.write(f"**Yuvarlanma (Roll):** {data['roll']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['roll'] + 30) / 60)))
    
    # Pitch Gauge
    st.write(f"**Yunuslama (Pitch):** {data['pitch']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['pitch'] + 30) / 60)))

# Charts
st.subheader("Uçuş Geçmişi")
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['time', 'altitude'])

new_row = pd.DataFrame({'time': [time.time()], 'altitude': [data['altitude']]})
st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(100)

st.line_chart(st.session_state.history.set_index('time'))

# Auto-refresh
time.sleep(0.1) # Faster refresh for smooth video
st.rerun()
