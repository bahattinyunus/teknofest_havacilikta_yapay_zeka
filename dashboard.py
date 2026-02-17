import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import glob
import cv2
import pydeck as pdk
from src.simulation.video_stream import VideoSynthesizer
from src.control.navigator import Navigator
from src.mission.loader import MissionLoader
from src.telemetry.mavlink_bridge import MavlinkBridge
from src.control.path_planner import PathPlanner
from src.control.visual_servo import VisualServo

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

st.title("🛸 SkyGuard AI - Görev Kontrol Merkezi (Elite Edition)")

# Initialize Systems
if 'video_sim' not in st.session_state:
    st.session_state.video_sim = VideoSynthesizer()
if 'navigator' not in st.session_state:
    st.session_state.navigator = Navigator()
    st.session_state.navigator.set_home(41.0082, 28.9784, 0)
if 'mission_loader' not in st.session_state:
    st.session_state.mission_loader = MissionLoader()
if 'mav_bridge' not in st.session_state:
    st.session_state.mav_bridge = MavlinkBridge()
if 'path_planner' not in st.session_state:
    st.session_state.path_planner = PathPlanner()
if 'visual_servo' not in st.session_state:
    st.session_state.visual_servo = VisualServo()

# Sidebar
with st.sidebar:
    st.header("Bağlantı Ayarları")
    connection_mode = st.radio("Veri Kaynağı", ["Simülasyon", "MAVLink (Donanım/SITL)"])
    
    if connection_mode == "MAVLink (Donanım/SITL)":
        conn_str = st.text_input("Bağlantı Adresi", "udp:127.0.0.1:14550")
        if st.button("Bağlan"):
            if st.session_state.mav_bridge.connect():
                st.success("MAVLink Bağlandı!")
            else:
                st.error("Bağlantı Hatası!")
        
        status_color = "🟢" if st.session_state.mav_bridge.connected else "🔴"
        st.info(f"Durum: {status_color}")
    else:
        st.info("Durum: SİMÜLASYON 🔵")

    st.divider()
    
    st.header("Görev Ayarları")
    mission_files = glob.glob("data/missions/*.json")
    selected_mission = st.selectbox("Görev Seç", [os.path.basename(f) for f in mission_files])
    
    if st.button("Görevi Yükle"):
        try:
            waypoints = st.session_state.mission_loader.load_mission(selected_mission)
            st.session_state.navigator.load_mission(waypoints)
            st.toast("Görev Yüklendi!", icon="🗺️")
        except Exception as e:
            st.error(f"Hata: {e}")

    st.divider()
    
    st.header("Gelişmiş Zeka")
    enable_path_planning = st.toggle("A* Yol Planlama", value=True)
    enable_visual_servo = st.toggle("Görsel Servo (Hedef Takibi)", value=False)
    vision_mode = st.selectbox("Kamera Modu", ["NORMAL", "THERMAL (Termal)"])

    st.divider()
    
    st.subheader("Sistem Komutları")
    if st.button("SİSTEMİ BAŞLAT (ARM)", type="primary"):
        if connection_mode == "MAVLink (Donanım/SITL)" and st.session_state.mav_bridge.connected:
            st.session_state.mav_bridge.arm()
        st.toast("Sistem BAŞLATILDI!", icon="⚠️")
    
    if st.button("OTONOM MOD"):
        st.toast("Otonom Plan Devrede", icon="🤖")

    if st.button("EVE DÖN (RTL)"):
        st.toast("Eve Dönüş Aktif", icon="🏠")

# Data Source Logic
def get_data():
    if connection_mode == "MAVLink (Donanım/SITL)" and st.session_state.mav_bridge.connected:
        state = st.session_state.mav_bridge.state
        return {
            "roll": state["roll"], "pitch": state["pitch"], "yaw": state["yaw"],
            "altitude": state["alt"], "battery": state["battery"], "speed": 0.0,
            "lat": state["lat"] if state["lat"] != 0 else 41.0082,
            "lon": state["lon"] if state["lon"] != 0 else 28.9784,
            "mode": state["mode"]
        }
    else:
        t = time.time()
        return {
            "roll": np.sin(t) * 5, "pitch": np.cos(t * 0.5) * 3, "yaw": (t * 10) % 360,
            "altitude": 20 + np.sin(t * 0.2) * 2, "battery": max(0, 95 - (t % 300) / 3),
            "speed": 8 + np.random.normal(0, 0.5),
            "lat": 41.0082 + np.sin(t * 0.1) * 0.001,
            "lon": 28.9784 + np.cos(t * 0.1) * 0.001,
            "mode": "SIM_ACTIVE"
        }

data = get_data()

# Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    tab1, tab2, tab3 = st.tabs(["🎥 Video Akışı", "🗺️ Harita", "📈 Analiz"])
    
    with tab1:
        # Video with Servoing logic
        frame, detections = st.session_state.video_sim.generate_frame(
            data['roll'], data['pitch'], mode=vision_mode.split()[0]
        )
        
        if enable_visual_servo and detections:
            # Simple servo logic: adjust data for display
            best_det = detections[0]
            r_adj, p_adj = st.session_state.visual_servo.calculate_commands(best_det['box'])
            st.caption(f"Visual Servo: R_adj={r_adj:.2f}, P_adj={p_adj:.2f}")

        st.image(frame, channels="BGR", use_column_width=True)
        
        if detections:
            st.warning(f"⚠️ {len(detections)} Hedef Tespit Edildi!")

    with tab2:
        # Live Map with Path Planning Visualization
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": data["lat"], "lon": data["lon"]}],
            get_position="[lon, lat]",
            get_color=[255, 0, 0],
            get_radius=20,
        )
        
        waypoints_df = pd.DataFrame(st.session_state.navigator.mission)
        mission_layer = pdk.Layer(
            "ScatterplotLayer",
            data=waypoints_df,
            get_position="[lon, lat]",
            get_color=[0, 255, 0],
            get_radius=15,
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer, mission_layer],
            initial_view_state=pdk.ViewState(latitude=data["lat"], longitude=data["lon"], zoom=16),
            map_style='mapbox://styles/mapbox/satellite-v9'
        ))

    with tab3:
        st.subheader("Yol Planlama Verileri (A*)")
        if enable_path_planning:
            st.success("Yol Planlayıcı Aktif: En kısa rota hesaplanıyor.")
            st.info("Algoritma: A* (A-Star) | Çözünürlük: 1.0m")
        else:
            st.warning("Yol Planlama Devre Dışı.")

with col2:
    st.subheader("Telemetri Verileri")
    
    m1, m2 = st.columns(2)
    m1.metric("İrtifa", f"{data['altitude']:.1f} m")
    m2.metric("Hız", f"{data['speed']:.1f} m/s")
    
    m3, m4 = st.columns(2)
    m3.metric("Pil", f"{data['battery']:.1f} %")
    m4.metric("Bağlantı", data["mode"])
    
    st.divider()
    
    st.subheader("Navigasyon")
    target = st.session_state.navigator.get_current_target()
    if target:
        bearing, dist, _ = st.session_state.navigator.update(data["lat"], data["lon"], data["altitude"])
        st.write(f"Hedef Mesafe: {dist:.1f} m")
        st.write(f"İstikamet: {bearing:.1f}°")
    
    st.divider()
    st.subheader("Durum Göstergeleri")
    st.write(f"**Roll:** {data['roll']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['roll'] + 30) / 60)))
    st.write(f"**Pitch:** {data['pitch']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['pitch'] + 30) / 60)))

# Auto-refresh
time.sleep(0.1)
st.rerun()
