import json
import os

class MissionLoader:
    def __init__(self, mission_dir="data/missions"):
        self.mission_dir = mission_dir
        os.makedirs(mission_dir, exist_ok=True)

    def load_mission(self, filename):
        path = os.path.join(self.mission_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Mission file not found: {path}")
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        return data.get("waypoints", [])

    def save_mission(self, filename, waypoints):
        path = os.path.join(self.mission_dir, filename)
        data = {"waypoints": waypoints}
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Test
    loader = MissionLoader()
    sample_mission = [
        {"lat": 41.0082, "lon": 28.9784, "alt": 10}, # Istanbul
        {"lat": 41.0090, "lon": 28.9790, "alt": 15},
        {"lat": 41.0100, "lon": 28.9800, "alt": 10}
    ]
    loader.save_mission("test_mission.json", sample_mission)
    print("Test mission saved.")
