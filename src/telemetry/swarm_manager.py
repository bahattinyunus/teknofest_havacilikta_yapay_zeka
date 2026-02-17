class SwarmManager:
    def __init__(self):
        self.drones = {} # ID -> State

    def update_drone(self, drone_id, state):
        self.drones[drone_id] = state

    def get_all_drones(self):
        return self.drones

    def get_swarm_center(self):
        if not self.drones:
            return None
        
        lats = [d['lat'] for d in self.drones.values()]
        lons = [d['lon'] for d in self.drones.values()]
        
        return {
            "lat": sum(lats) / len(lats),
            "lon": sum(lons) / len(lons)
        }
