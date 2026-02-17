import cv2
import numpy as np
import time

class VideoSynthesizer:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.targets = []
        self.last_target_time = time.time()
        self.mode = "NORMAL" # NORMAL, THERMAL

    def generate_frame(self, roll, pitch, mode="NORMAL"):
        """
        Generate a synthetic frame based on roll and pitch.
        """
        self.mode = mode
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        horizon_y = int(self.height / 2 + pitch * 10)
        
        if self.mode == "NORMAL":
            # Sky
            cv2.rectangle(frame, (0, 0), (self.width, horizon_y), (235, 206, 135), -1) # Sky Blue
            # Ground
            cv2.rectangle(frame, (0, horizon_y), (self.width, self.height), (100, 150, 50), -1) # Grass Green
            grid_color = (80, 120, 40)
        else:
            # Thermal Mode (White Hot)
            # Sky is colder (darker), ground is warmer (middle gray)
            cv2.rectangle(frame, (0, 0), (self.width, horizon_y), (50, 50, 50), -1) 
            cv2.rectangle(frame, (0, horizon_y), (self.width, self.height), (120, 120, 120), -1)
            grid_color = (130, 130, 130)

        # Artificial Grid
        self._draw_grid(frame, horizon_y, roll, grid_color)
        
        # Simulate Targets
        self._update_targets()
        detections = []
        
        for t in self.targets:
            x, y, w, h = t['box']
            y_adj = y + pitch * 5
            
            if 0 < y_adj < self.height - h:
                if self.mode == "NORMAL":
                    cv2.rectangle(frame, (x, int(y_adj)), (x+w, int(y_adj+h)), (0, 0, 255), -1)
                else:
                    # Thermal: Targets are very hot (bright white)
                    cv2.rectangle(frame, (x, int(y_adj)), (x+w, int(y_adj+h)), (255, 255, 255), -1)
                    # Add heat glow
                    cv2.GaussianBlur(frame[max(0, int(y_adj-10)):min(self.height, int(y_adj+h+10)), 
                                          max(0, x-10):min(self.width, x+w+10)], (15, 15), 0)
                
                # Mock Detection
                detections.append({
                    'class_name': 'Insan',
                    'confidence': 0.85 + np.random.random() * 0.1,
                    'box': [x, y_adj, w, h],
                    'centroid': (x + w/2, y_adj + h/2)
                })

        # HUD Overlay
        self._draw_hud(frame, roll, pitch)
        
        return frame, detections

    def _draw_grid(self, frame, horizon_y, roll, color):
        center_x = self.width // 2
        for i in range(-5, 6):
            start_point = (center_x + i * 100 + int(roll * 5), self.height)
            end_point = (center_x + i * 20, horizon_y)
            cv2.line(frame, start_point, end_point, color, 1)

    def _update_targets(self):
        if time.time() - self.last_target_time > 3.0:
            self.targets.append({
                'box': [np.random.randint(50, self.width-50), np.random.randint(self.height//2, self.height-50), 30, 60],
                'type': 'person'
            })
            self.last_target_time = time.time()
            
        if len(self.targets) > 5:
            self.targets.pop(0)

    def _draw_hud(self, frame, roll, pitch):
        center_y = self.height // 2
        center_x = self.width // 2
        hud_color = (0, 255, 0) if self.mode == "NORMAL" else (200, 200, 200)
        
        # Crosshair
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), hud_color, 1)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), hud_color, 1)
        
        # Info
        cv2.putText(frame, f"MODE: {self.mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hud_color, 1)
        cv2.putText(frame, f"R: {roll:.1f} P: {pitch:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, hud_color, 1)
