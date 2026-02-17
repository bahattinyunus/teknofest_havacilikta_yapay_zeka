import cv2
import numpy as np
from ultralytics import YOLO
import time

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.5):
        """
        Initialize the ObjectDetector with a YOLOv8 model.
        
        Args:
            model_path (str): Path to the YOLOv8 model file.
            conf_threshold (float): Confidence threshold for detections.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.colors = np.random.uniform(0, 255, size=(100, 3))

    def detect(self, frame):
        """
        Perform object detection on a single frame.
        
        Args:
            frame (numpy.ndarray): Input image frame.
            
        Returns:
            list: List of detections (class_id, confidence, box).
            numpy.ndarray: Annotated frame.
        """
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        annotated_frame = frame.copy()
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                cls = int(box.cls[0].cpu().numpy())
                
                detections.append({
                    'class_id': cls,
                    'class_name': self.model.names[cls],
                    'confidence': float(conf),
                    'box': [float(x1), float(y1), float(x2), float(y2)]
                })

                # Draw bounding box
                color = self.colors[cls % len(self.colors)]
                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                label = f"{self.model.names[cls]} {conf:.2f}"
                cv2.putText(annotated_frame, label, (int(x1), int(y1) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            
        return detections, annotated_frame

    def run_on_video(self, source=0):
        """
        Run detection on a video source (webcam or file).
        """
        cap = cv2.VideoCapture(source)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            detections, annotated_frame = self.detect(frame)
            
            cv2.imshow('SkyGuard AI - Vision', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test with default webcam
    detector = ObjectDetector()
    detector.run_on_video()
