import numpy as np
import time

class VisualServo:
    def __init__(self, kp_roll=0.08, ki_roll=0.01, kd_roll=0.02, 
                 kp_pitch=0.08, ki_pitch=0.01, kd_pitch=0.02, 
                 center_x=320, center_y=240):
        self.kp_roll, self.ki_roll, self.kd_roll = kp_roll, ki_roll, kd_roll
        self.kp_pitch, self.ki_pitch, self.kd_pitch = kp_pitch, ki_pitch, kd_pitch
        self.center_x = center_x
        self.center_y = center_y
        
        # PID States
        self.prev_error_x = 0
        self.integral_x = 0
        self.prev_error_y = 0
        self.integral_y = 0
        self.last_time = time.time()

    def calculate_commands(self, target_bbox):
        """
        target_bbox: [x, y, w, h]
        Returns: roll_adjustment, pitch_adjustment
        """
        if target_bbox is None:
            self.integral_x = 0
            self.integral_y = 0
            return 0, 0

        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0: dt = 0.01

        target_x = target_bbox[0] + target_bbox[2] / 2
        target_y = target_bbox[1] + target_bbox[3] / 2

        error_x = target_x - self.center_x
        error_y = target_y - self.center_y

        # PID for X (Roll)
        self.integral_x += error_x * dt
        self.integral_x = np.clip(self.integral_x, -10, 10) # Anti-windup
        derivative_x = (error_x - self.prev_error_x) / dt
        roll_adj = -(self.kp_roll * error_x + self.ki_roll * self.integral_x + self.kd_roll * derivative_x)

        # PID for Y (Pitch)
        self.integral_y += error_y * dt
        self.integral_y = np.clip(self.integral_y, -10, 10) # Anti-windup
        derivative_y = (error_y - self.prev_error_y) / dt
        pitch_adj = (self.kp_pitch * error_y + self.ki_pitch * self.integral_y + self.kd_pitch * derivative_y)

        self.prev_error_x = error_x
        self.prev_error_y = error_y
        self.last_time = current_time

        return np.clip(roll_adj, -1.0, 1.0), np.clip(pitch_adj, -1.0, 1.0)
