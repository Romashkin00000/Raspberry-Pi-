import cv2

class PlateDetector:
    def __init__(self, cascade_path):
        self.plate_cascade = cv2.CascadeClassifier(cascade_path)

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = self.plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return len(plates) > 0