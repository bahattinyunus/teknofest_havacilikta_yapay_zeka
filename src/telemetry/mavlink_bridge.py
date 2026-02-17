import time
import threading
from pymavlink import mavutil

class MavlinkBridge:
    def __init__(self, connection_string="udp:127.0.0.1:14550", baud=57600):
        """
        Initialize MAVLink connection.
        
        Args:
            connection_string (str): Connection string (e.g., 'COM3', 'udp:127.0.0.1:14550')
            baud (int): Baud rate for serial connections.
        """
        self.connection_string = connection_string
        self.baud = baud
        self.master = None
        self.connected = False
        self.state = {
            "lat": 0, "lon": 0, "alt": 0,
            "roll": 0, "pitch": 0, "yaw": 0,
            "battery": 0, "mode": "UNKNOWN"
        }
        self._stop_event = threading.Event()
        self._thread = None

    def connect(self):
        print(f"Connecting to MAVLink on {self.connection_string}...")
        try:
            self.master = mavutil.mavlink_connection(self.connection_string, baud=self.baud)
            self.master.wait_heartbeat()
            self.connected = True
            print("Heartbeat received! Connected to MAVLink.")
            
            # Start listener thread
            self._thread = threading.Thread(target=self._listener_loop, daemon=True)
            self._thread.start()
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def disconnect(self):
        self._stop_event.set()
        if self.master:
            self.master.close()
        self.connected = False

    def _listener_loop(self):
        while not self._stop_event.is_set():
            try:
                msg = self.master.recv_match(blocking=True, timeout=1.0)
                if not msg:
                    continue

                msg_type = msg.get_type()
                
                if msg_type == 'GLOBAL_POSITION_INT':
                    self.state["lat"] = msg.lat / 1e7
                    self.state["lon"] = msg.lon / 1e7
                    self.state["alt"] = msg.relative_alt / 1000.0 # mm to m

                elif msg_type == 'ATTITUDE':
                    self.state["roll"] = msg.roll * 57.2958 # rad to deg
                    self.state["pitch"] = msg.pitch * 57.2958
                    self.state["yaw"] = msg.yaw * 57.2958

                elif msg_type == 'SYS_STATUS':
                    self.state["battery"] = msg.battery_remaining
                    
                elif msg_type == 'HEARTBEAT':
                    mode_id = msg.custom_mode
                    # Simplified mode mapping
                    self.state["mode"] = f"MODE_{mode_id}"

            except Exception as e:
                print(f"MAVLink Error: {e}")

    def arm(self):
        if not self.connected: return
        self.master.arducopter_arm()
        self.master.motors_armed_wait()
        print("MAVLink: ARMED")

    def disarm(self):
        if not self.connected: return
        self.master.arducopter_disarm()
        self.master.motors_disarmed_wait()
        print("MAVLink: DISARMED")

    def set_mode(self, mode="GUIDED"):
        if not self.connected: return
        mode_id = self.master.mode_mapping()[mode]
        self.master.set_mode(mode_id)
        print(f"MAVLink: Mode set to {mode}")

    def takeoff(self, altitude=10):
        if not self.connected: return
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, altitude
        )
        print(f"MAVLink: Takeoff to {altitude}m")

if __name__ == "__main__":
    # Test with SITL
    bridge = MavlinkBridge()
    if bridge.connect():
        time.sleep(2)
        print(f"State: {bridge.state}")
        bridge.disconnect()
