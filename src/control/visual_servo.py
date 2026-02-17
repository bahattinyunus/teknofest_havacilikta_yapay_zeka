import numpy as np

class VisualServo:
    def __init__(self, kp_roll=0.05, kp_pitch=0.05, center_x=320, center_y=240):
        self.kp_roll = kp_roll
        self.kp_pitch = kp_pitch
        self.center_x = center_x
        self.center_y = center_y

    def calculate_commands(self, target_bbox):
        """
        target_bbox: [x, y, w, h]
        Returns: roll_adjustment, pitch_adjustment
        """
        if target_bbox is None:
            return 0, 0

        target_x = target_bbox[0] + target_bbox[2] / 2
        target_y = target_bbox[1] + target_bbox[3] / 2

        error_x = target_x - self.center_x
        error_y = target_y - self.center_y

        # Simple proportional control to center the target
        roll_adj = -error_x * self.kp_roll
        pitch_adj = error_y * self.kp_pitch # Pitch up if target is above center? Adjust polarity as needed

        return roll_adj, pitch_adj
