import time
import argparse
import sys
import threading
import numpy as np
from src.vision.detector import ObjectDetector
from src.control.flight_controller import FlightController
from src.control.path_planner import PathPlanner
from src.mission.loader import MissionLoader
from src.telemetry.logger import TelemetryLogger

def main(mission_file=None):
    print("SkyGuard AI Baslatiliyor...")
    
    # Initialize modules
    try:
        detector = ObjectDetector() # Will create dummy if model not found
        controller = FlightController()
        logger = TelemetryLogger()
        planner = PathPlanner(grid_size=(100, 100), resolution=1.0) # 100x100m area
        mission_loader = MissionLoader()
        
        print("Moduller basariyla yuklendi.")
    except Exception as e:
        print(f"Moduller baslatilirken hata: {e}")
        return

    # Load Mission
    waypoints = []
    if mission_file:
        try:
            waypoints = mission_loader.load_mission(mission_file)
            print(f"Gorev yuklendi: {len(waypoints)} nokta.")
        except Exception as e:
            print(f"Gorev yuklenemedi: {e}")
    else:
        # Default simple patrol box
        waypoints = [
            {"lat": 0, "lon": 0, "alt": 10, "x": 0, "y": 0},
            {"lat": 0, "lon": 0, "alt": 10, "x": 10, "y": 0},
            {"lat": 0, "lon": 0, "alt": 10, "x": 10, "y": 10},
            {"lat": 0, "lon": 0, "alt": 10, "x": 0, "y": 10},
        ]
        print("Varsayilan devriye gorevi yuklendi.")

    # Simulation loop
    print("Ana Dongu Baslatiliyor...")
    controller.arm()
    
    current_wp_index = 0
    path = None
    
    # State simulation vars
    sim_x, sim_y, sim_z = 0.0, 0.0, 0.0
    
    try:
        while True:
            # 1. Sense: Simulating state
            current_state = {
                "roll": 0.0,
                "pitch": 0.0,
                "yaw": 0.0,
                "altitude": sim_z,
                "battery": 95.0,
                "mode": controller.state["mode"],
                "x": sim_x,
                "y": sim_y
            }
            controller.update_state(current_state)
            
            # 2. Perceive: Vision
            # In a real scenario, this would detect objects
            detections = [] 
            
            # 3. Plan & Act
            if current_wp_index < len(waypoints):
                target_wp = waypoints[current_wp_index]
                target_pos = (target_wp.get('x', 0), target_wp.get('y', 0))
                
                # Check arrival
                dist = np.sqrt((sim_x - target_pos[0])**2 + (sim_y - target_pos[1])**2)
                
                if dist < 1.0:
                    print(f"Noktaya ulasildi: {current_wp_index}")
                    current_wp_index += 1
                else:
                    # Plan path if needed (simple straight line for now or A*)
                    # Real A* usage:
                    # if not path:
                    #     path = planner.plan((sim_x, sim_y), target_pos)
                    
                    # Move towards target (Simulation logic, NOT control logic)
                    dx = target_pos[0] - sim_x
                    dy = target_pos[1] - sim_y
                    
                    # Normalize
                    mag = np.sqrt(dx**2 + dy**2)
                    if mag > 0:
                        sim_x += (dx/mag) * 0.5 # 0.5 m/s speed
                        sim_y += (dy/mag) * 0.5
                    
                    sim_z = target_wp.get('alt', 10)
                    
                    # Controller Output (for logging)
                    targets = controller.navigate_to(sim_x, sim_y, sim_z)
                    
            else:
                print("Gorev Tamamlandi.", end='\r')
                # Hover or Land
                targets = {"roll": 0, "pitch": 0, "yaw": 0, "altitude": 0}
            
            motor_outputs = controller.calculate_motor_outputs(targets)
            
            # 4. Log
            logger.log(current_state, detections)
            
            # 5. Output status
            print(f"Durum: {current_state['mode']} | Pos: ({sim_x:.1f}, {sim_y:.1f}) | WP: {current_wp_index}/{len(waypoints)}", end='\r')
            
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
