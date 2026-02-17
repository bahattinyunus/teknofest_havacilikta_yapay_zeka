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

# Initialize Systems
if 'video_sim' not in st.session_state:
    st.session_state.video_sim = VideoSynthesizer()
if 'navigator' not in st.session_state:
    st.session_state.navigator = Navigator()
    # Default Home (Istanbul Teknofest Area)
    st.session_state.navigator.set_home(41.0082, 28.9784, 0)
if 'mission_loader' not in st.session_state:
    st.session_state.mission_loader = MissionLoader()
if 'mav_bridge' not in st.session_state:
    st.session_state.mav_bridge = MavlinkBridge()

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
        
        if st.session_state.mav_bridge.connected:
            st.info("Durum: BAĞLI 🟢")
        else:
            st.warning("Durum: AYRIK 🔴")
    else:
        st.info("Durum: SİMÜLASYON 🔵")

    st.divider()
    
    st.header("Sistem Durumu")
    
    st.subheader("Görev Yöneticisi")
    mission_files = glob.glob("data/missions/*.json")
    selected_mission = st.selectbox("Görev Seç", [os.path.basename(f) for f in mission_files])
    
    if st.button("Görevi Yükle"):
        try:
            waypoints = st.session_state.mission_loader.load_mission(selected_mission)
            st.session_state.navigator.load_mission(waypoints)
            st.toast(f"{len(waypoints)} Noktalı Görev Yüklendi!", icon="🗺️")
        except Exception as e:
            st.error(f"Hata: {e}")

    st.divider()
    
    st.subheader("Uçuş Kontrolü")
    if st.button("SİSTEMİ BAŞLAT (ARM)", type="primary"):
        if connection_mode == "MAVLink (Donanım/SITL)" and st.session_state.mav_bridge.connected:
            st.session_state.mav_bridge.arm()
            st.toast("MAVLink: ARM Komutu Gönderildi", icon="⚠️")
        else:
            st.toast("Sistem BAŞLATILDI (ARMED)!", icon="⚠️")
    
    if st.button("OTONOM GÖREVİ BAŞLAT"):
        st.toast("Otonom Mod Aktif", icon="🤖")

    if st.button("EVE DÖN (RTL)"):
        if connection_mode == "MAVLink (Donanım/SITL)" and st.session_state.mav_bridge.connected:
             st.session_state.mav_bridge.set_mode("RTL")
             st.toast("MAVLink: RTL Moduna Geçildi", icon="🏠")
        else:
            st.toast("Eve Dönüş Modu Aktif", icon="🏠")

# Data Source Logic
def get_data():
    if connection_mode == "MAVLink (Donanım/SITL)" and st.session_state.mav_bridge.connected:
        state = st.session_state.mav_bridge.state
        return {
            "roll": state["roll"],
            "pitch": state["pitch"],
            "yaw": state["yaw"],
            "altitude": state["alt"],
            "battery": state["battery"],
            "speed": 0.0, # Adding speed to mavlink bridge later
            "lat": state["lat"] if state["lat"] != 0 else 41.0082,
            "lon": state["lon"] if state["lon"] != 0 else 28.9784,
            "mode": state["mode"]
        }
    else:
        # Simulation
        t = time.time()
        lat = 41.0082 + np.sin(t * 0.1) * 0.001
        lon = 28.9784 + np.cos(t * 0.1) * 0.001
        return {
            "roll": np.sin(t) * 5,
            "pitch": np.cos(t * 0.5) * 3,
            "yaw": (t * 10) % 360,
            "altitude": 20 + np.sin(t * 0.2) * 2,
            "battery": max(0, 95 - (t % 300) / 3),
            "speed": 8 + np.random.normal(0, 0.5),
            "lat": lat,
            "lon": lon,
            "mode": "SIMULATION"
        }

data = get_data()

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    tab1, tab2 = st.tabs(["Canlı İzleme", "Harita Görünümü"])
    
    with tab1:
        st.subheader("Görüntü İşleme ve Takip")
        video_placeholder = st.empty()
        # Generate Frame
        frame, detections = st.session_state.video_sim.generate_frame(data['roll'], data['pitch'])
        video_placeholder.image(frame, channels="BGR", use_column_width=True)
        
        if detections:
            st.warning(f"⚠️ {len(detections)} Hedef Tespit Edildi!")

    with tab2:
        st.subheader("Canlı Harita")
        
        # Flight Path
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": data["lat"], "lon": data["lon"]}],
            get_position="[lon, lat]",
            get_color=[255, 0, 0],
            get_radius=20,
        )
        
        # Mission Waypoints
        waypoints_df = pd.DataFrame(st.session_state.navigator.mission)
        mission_layer = pdk.Layer(
            "ScatterplotLayer",
            data=waypoints_df,
            get_position="[lon, lat]",
            get_color=[0, 255, 0],
            get_radius=15,
        )

        view_state = pdk.ViewState(
            latitude=data["lat"],
            longitude=data["lon"],
            zoom=16,
            pitch=0,
        )
        
        st.pydeck_chart(pdk.Deck(
            layers=[layer, mission_layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/satellite-v9'
        ))

with col2:
    st.subheader("Telemetri")
    
    m1, m2 = st.columns(2)
    m1.metric("İrtifa (AGL)", f"{data['altitude']:.1f} m", "0.1 m")
    m2.metric("Yer Hızı", f"{data['speed']:.1f} m/s", "-0.2 m/s")
    
    m3, m4 = st.columns(2)
    m3.metric("Pil", f"{data['battery']:.1f} %", "-0.1 %")
    m4.metric("Mod", data["mode"])
    
    st.divider()
    
    st.write(f"**Konum:** {data['lat']:.6f}, {data['lon']:.6f}")
    
    st.subheader("Navigasyon")
    target = st.session_state.navigator.get_current_target()
    if target:
        st.info(f"Hedef: WP-{st.session_state.navigator.current_waypoint_index}")
        bearing, dist, _ = st.session_state.navigator.update(data["lat"], data["lon"], data["altitude"])
        st.write(f"Mesafe: {dist:.1f} m")
        st.write(f"İstikamet: {bearing:.1f}°")
    else:
        st.warning("Aktif Görev Yok")

    st.divider()
    st.subheader("Yönelim")
    st.write(f"**Roll:** {data['roll']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['roll'] + 30) / 60)))
    
    st.write(f"**Pitch:** {data['pitch']:.2f}°")
    st.progress(min(1.0, max(0.0, (data['pitch'] + 30) / 60)))

# Auto-refresh
time.sleep(0.1)
st.rerun()
