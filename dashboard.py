import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import glob
import cv2

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
    st.subheader("Canlı Video Akışı (Simülasyon)")
    # Placeholder for video stream
    video_placeholder = st.empty()
    
    # Simulate video feed
    # In real app, this would pull from a camera stream or websocket
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "SINYAL YOK", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    video_placeholder.image(img, channels="BGR", use_column_width=True)

with col2:
    st.subheader("Telemetri")
    
    # Live metrics
    data = get_mock_data()
    
    m1, m2 = st.columns(2)
    m1.metric("İrtifa", f"{data['altitude']:.1f} m", "0.1 m")
    m2.metric("Yer Hızı", f"{data['speed']:.1f} m/s", "-0.2 m/s")
    
    m3, m4 = st.columns(2)
    m3.metric("Pil", f"{data['battery']:.1f} %", "-0.1 %")
    m4.metric("Bağlantı Kalitesi", "98 %", "0 %")
    
    st.divider()
    
    st.subheader("Yönelim (Attitude)")
    st.write(f"**Yuvarlanma (Roll):** {data['roll']:.2f}°")
    st.progress((data['roll'] + 30) / 60)
    
    st.write(f"**Yunuslama (Pitch):** {data['pitch']:.2f}°")
    st.progress((data['pitch'] + 30) / 60)

# Charts
st.subheader("Uçuş Geçmişi")
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['time', 'altitude'])

new_row = pd.DataFrame({'time': [time.time()], 'altitude': [data['altitude']]})
st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(100)

st.line_chart(st.session_state.history.set_index('time'))

# Auto-refresh
time.sleep(1)
st.rerun()
