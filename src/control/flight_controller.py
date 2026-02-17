import time
import numpy as np

class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.time()

    def update(self, current_value):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0: return 0

        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.prev_error = error
        self.last_time = current_time
        
        return output

class FlightController:
    def __init__(self):
        # Initialize PIDs for Roll, Pitch, Yaw, Altitude
        self.roll_pid = PIDController(1.0, 0.0, 0.0)
        self.pitch_pid = PIDController(1.0, 0.0, 0.0)
        self.yaw_pid = PIDController(1.5, 0.1, 0.05)
        self.altitude_pid = PIDController(2.0, 0.5, 0.1)
        
        self.state = {
            "roll": 0.0,
            "pitch": 0.0,
            "yaw": 0.0,
            "altitude": 0.0,
            "battery": 100.0,
            "mode": "DISARMED"
        }

    def update_state(self, new_state):
        """Update the internal state estimate."""
        self.state.update(new_state)

    def calculate_motor_outputs(self, targets):
        """
        Calculate motor outputs based on target orientation/position.
        
        Args:
            targets (dict): Target values for roll, pitch, yaw, altitude.
        """
        self.roll_pid.setpoint = targets.get("roll", 0)
        self.pitch_pid.setpoint = targets.get("pitch", 0)
        self.yaw_pid.setpoint = targets.get("yaw", 0)
        self.altitude_pid.setpoint = targets.get("altitude", 0)

        roll_out = self.roll_pid.update(self.state["roll"])
        pitch_out = self.pitch_pid.update(self.state["pitch"])
        yaw_out = self.yaw_pid.update(self.state["yaw"])
        alt_out = self.altitude_pid.update(self.state["altitude"])
        
        # Mixing logic for a quadcopter (X configuration)
        # Front Left  (1): Throttle + Roll + Pitch - Yaw
        # Front Right (2): Throttle - Roll + Pitch + Yaw
        # Rear Left   (3): Throttle + Roll - Pitch + Yaw
        # Rear Right  (4): Throttle - Roll - Pitch - Yaw
        
        throttle_base = 1500 + alt_out # Base PWM
        
        m1 = throttle_base + roll_out + pitch_out - yaw_out
        m2 = throttle_base - roll_out + pitch_out + yaw_out
        m3 = throttle_base + roll_out - pitch_out + yaw_out
        m4 = throttle_base - roll_out - pitch_out - yaw_out
        
        return {
            "m1": np.clip(m1, 1000, 2000),
            "m2": np.clip(m2, 1000, 2000),
            "m3": np.clip(m3, 1000, 2000),
            "m4": np.clip(m4, 1000, 2000)
        }

    def arm(self):
        self.state["mode"] = "ARMED"
        print("System ARMED")

    def disarm(self):
        self.state["mode"] = "DISARMED"
        print("System DISARMED")

    def navigate_to(self, x, y, z, check_arrival=False, arrival_threshold=1.0):
        """
        Simple navigation wrapper. In a real controller, this would update setpoints.
        Returns true if arrived (if check_arrival is True).
        """
        # For this simulation level, we assume direct setpoint control
        # In reality, you'd generate velocity commands from position error
        
        self.roll_pid.setpoint = 0 # Hover
        self.pitch_pid.setpoint = 0 
        self.yaw_pid.setpoint = 0
        self.altitude_pid.setpoint = z
        
        # We don't have a position PID in this simple class, 
        # so we just return the theoretical motor outputs for hovering at Z
        # The higher level loop handles X/Y via pitch/roll or just assumes 
        # the 'drone' moves there (kinematics in gym_env).
        
        return {
            "roll": 0, 
            "pitch": 0, 
            "yaw": 0, 
            "altitude": z
        }
