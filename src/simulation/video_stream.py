import cv2
import numpy as np
import time

class VideoSynthesizer:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.horizon_color = (255, 200, 100) # Light blue-ish
        self.ground_color = (30, 100, 30) # Dark green
        self.targets = []
        self.last_target_time = time.time()

    def generate_frame(self, roll, pitch):
        """
        Generate a synthetic frame based on roll and pitch.
        """
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Simple horizon simulation
        # Pitch shifts the horizon up/down
        # Roll rotates the horizon (simplified as lines for performance)
        
        horizon_y = int(self.height / 2 + pitch * 10)
        
        # Sky
        cv2.rectangle(frame, (0, 0), (self.width, horizon_y), (235, 206, 135), -1) # Sky Blue
        
        # Ground
        cv2.rectangle(frame, (0, horizon_y), (self.width, self.height), (100, 150, 50), -1) # Grass Green
        
        # Artificial Grid to show movement
        self._draw_grid(frame, horizon_y, roll)
        
        # Simulate Targets
        self._update_targets()
        detections = []
        
        for t in self.targets:
            # Draw target
            x, y, w, h = t['box']
            # Adjust y based on pitch for simple 3D effect
            y_adj = y + pitch * 5
            
            if 0 < y_adj < self.height - h:
                cv2.rectangle(frame, (x, int(y_adj)), (x+w, int(y_adj+h)), (0, 0, 255), -1)
                
                # Mock Detection
                detections.append({
                    'class_name': 'Insan',
                    'confidence': 0.85 + np.random.random() * 0.1,
                    'box': [x, y_adj, x+w, y_adj+h]
                })

        # HUD Overlay
        self._draw_hud(frame, roll, pitch)
        
        return frame, detections

    def _draw_grid(self, frame, horizon_y, roll):
        # Draw perspective lines on ground
        center_x = self.width // 2
        for i in range(-5, 6):
            # Perspective lines radiating from center horizon
            start_point = (center_x + i * 100 + int(roll * 5), self.height)
            end_point = (center_x + i * 20, horizon_y)
            cv2.line(frame, start_point, end_point, (80, 120, 40), 2)

    def _update_targets(self):
        # Add new target occasionally
        if time.time() - self.last_target_time > 3.0:
            self.targets.append({
                'box': [np.random.randint(50, self.width-50), np.random.randint(self.height//2, self.height-50), 30, 60],
                'type': 'person'
            })
            self.last_target_time = time.time()
            
        # Remove old targets
        if len(self.targets) > 3:
            self.targets.pop(0)

    def _draw_hud(self, frame, roll, pitch):
        # Artificial Horizon Line
        center_y = self.height // 2
        center_x = self.width // 2
        
        # Crosshair
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 0), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 0), 2)
        
        # Info
        cv2.putText(frame, f"R: {roll:.1f} P: {pitch:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

if __name__ == "__main__":
    sim = VideoSynthesizer()
    while True:
        frame, _ = sim.generate_frame(0, 0)
        cv2.imshow("Sim", frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
