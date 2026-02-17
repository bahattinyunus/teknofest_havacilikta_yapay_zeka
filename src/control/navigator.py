import math

class Navigator:
    def __init__(self):
        self.home_location = None
        self.current_waypoint_index = 0
        self.mission = []
        self.acceptance_radius = 2.0 # meters

    def set_home(self, lat, lon, alt):
        self.home_location = {"lat": lat, "lon": lon, "alt": alt}

    def load_mission(self, mission_waypoints):
        """
        Load a list of waypoints.
        Each waypoint: {"lat": float, "lon": float, "alt": float}
        """
        self.mission = mission_waypoints
        self.current_waypoint_index = 0

    def get_current_target(self):
        if not self.mission or self.current_waypoint_index >= len(self.mission):
            return None
        return self.mission[self.current_waypoint_index]

    def update(self, current_lat, current_lon, current_alt):
        """
        Update navigation state based on current position.
        Returns target_bearing, target_distance, target_altitude
        """
        target = self.get_current_target()
        if not target:
            return 0, 0, 0

        dist = self._haversine_distance(current_lat, current_lon, target["lat"], target["lon"])
        bearing = self._calculate_bearing(current_lat, current_lon, target["lat"], target["lon"])
        
        # Check if reached
        if dist < self.acceptance_radius and abs(current_alt - target["alt"]) < 1.0:
            print(f"Waypoint {self.current_waypoint_index} reached!")
            self.current_waypoint_index += 1
            
        return bearing, dist, target["alt"]

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000 # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def _calculate_bearing(self, lat1, lon1, lat2, lon2):
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dlambda = math.radians(lon2 - lon1)

        y = math.sin(dlambda) * math.cos(phi2)
        x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlambda)
        theta = math.atan2(y, x)
        return (math.degrees(theta) + 360) % 360
