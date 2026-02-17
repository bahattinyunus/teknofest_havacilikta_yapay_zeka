import time
import argparse
import sys
import threading
from src.vision.detector import ObjectDetector
from src.control.flight_controller import FlightController
from src.telemetry.logger import TelemetryLogger

def main(mission_file=None):
    print("SkyGuard AI Baslatiliyor...")
    
    # Initialize modules
    try:
        detector = ObjectDetector() # Will create dummy if model not found
        controller = FlightController()
        logger = TelemetryLogger()
        print("Moduller basariyla yuklendi.")
    except Exception as e:
        print(f"Moduller baslatilirken hata: {e}")
        return

    # Simulation loop
    print("Ana Dongu Baslatiliyor...")
    controller.arm()
    
    try:
        while True:
            # 1. Sense: In a real scenario, getting data from sensors/camera
            # Simulating data for now
            current_state = {
                "roll": 0.0,
                "pitch": 0.0,
                "yaw": 0.0,
                "altitude": 10.0, # Hovering at 10m
                "battery": 95.0,
                "mode": controller.state["mode"]
            }
            controller.update_state(current_state)
            
            # 2. Perceive: Vision processing (Simulated frame or real cam)
            # In real implementations, this would grab a frame from the camera
            detections = [] 
            # detections, _ = detector.detect(current_frame) 

            # 3. Plan & Act: Control Logic
            # Example target: Hold position
            targets = {"roll": 0, "pitch": 0, "yaw": 0, "altitude": 10}
            motor_outputs = controller.calculate_motor_outputs(targets)
            
            # 4. Log
            logger.log(current_state, detections)
            
            # 5. Output status
            print(f"Durum: {current_state['mode']} | Irtifa: {current_state['altitude']}m | Motorlar: {motor_outputs}", end='\r')
            
            time.sleep(0.1) # 10Hz loop
            
    except KeyboardInterrupt:
        print("\nSkyGuard AI Durduruluyor...")
        controller.disarm()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkyGuard AI Ana Kontrol Dongusu")
    parser.add_argument("--mission", type=str, help="Gorev dosyasi yolu (JSON)")
    args = parser.parse_args()
    
    main(args.mission)
