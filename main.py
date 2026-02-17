import time
import argparse
import sys
import threading
from src.vision.detector import ObjectDetector
from src.control.flight_controller import FlightController
from src.telemetry.logger import TelemetryLogger

def main(mission_file=None):
    print("Initializing SkyGuard AI...")
    
    # Initialize modules
    try:
        detector = ObjectDetector() # Will create dummy if model not found
        controller = FlightController()
        logger = TelemetryLogger()
        print("Modules loaded successfully.")
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return

    # Simulation loop
    print("Starting Main Loop...")
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
            print(f"Status: {current_state['mode']} | Alt: {current_state['altitude']}m | Motors: {motor_outputs}", end='\r')
            
            time.sleep(0.1) # 10Hz loop
            
    except KeyboardInterrupt:
        print("\nStopping SkyGuard AI...")
        controller.disarm()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkyGuard AI Main Control Loop")
    parser.add_argument("--mission", type=str, help="Path to mission file (JSON)")
    args = parser.parse_args()
    
    main(args.mission)
