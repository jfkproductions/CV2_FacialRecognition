# face_detector.py
import os
import cv2
import dlib  # dlib is needed for CNN and HOG

class FaceDetector:
    def __init__(self, method, classifier_name, upload_folder, processed_folder, rect_thickness=2):
        self.method = method
        self.classifier_name = classifier_name
        self.upload_folder = upload_folder
        self.processed_folder = processed_folder
        self.rect_thickness = rect_thickness

        # Paths to Haarcascade models
        self.cascade_paths = {
            'Faces': 'haarcascade_frontalface_default.xml',
            'Eyes': 'haarcascade_eye.xml',
            'Cars': 'cars.xml',
            'Clocks': 'clocks.xml',
            'Fullbody': 'fullbody.xml'
        }

        if self.method == 'haarcascade':
            cascade_file = self.cascade_paths.get(self.classifier_name, 'haarcascade_frontalface_default.xml')
            cascade_path = os.path.join('models/haarcascade/', cascade_file)
            self.classifier = cv2.CascadeClassifier(cascade_path)
        elif self.method == 'HOG':
            # Load HOG face detector from dlib
            self.classifier = dlib.get_frontal_face_detector()
        elif self.method == 'CNN':
            # Load CNN face detector from dlib with the correct weights file
            cnn_model = os.path.join('weights/', 'mmod_human_face_detector.dat')  # Ensure this file exists
            self.classifier = dlib.cnn_face_detection_model_v1(cnn_model)
        else:
            self.classifier = None

    def detect(self, image_path, filename, scale_factor=1.1, min_neighbors=5, upsample_times=1):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (800, 600))
        detections = []

        if self.method == 'haarcascade' and self.classifier is not None:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detections = self.classifier.detectMultiScale(
                gray_image,
                scaleFactor=scale_factor,
                minNeighbors=min_neighbors
            )
            for (x, y, w, h) in detections:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), self.rect_thickness)

        elif self.method == 'HOG' and self.classifier is not None:
            # No need to convert to RGB as per your notebook code
            detections = self.classifier(image, upsample_times)
            for face in detections:
                l, t, r, b = face.left(), face.top(), face.right(), face.bottom()
                cv2.rectangle(image, (l, t), (r, b), (0, 255, 255), self.rect_thickness)

        elif self.method == 'CNN' and self.classifier is not None:
            # No need to convert to RGB as per your notebook code
            detections = self.classifier(image, upsample_times)
            for face in detections:
                l, t, r, b = face.rect.left(), face.rect.top(), face.rect.right(), face.rect.bottom()
                confidence = face.confidence
                cv2.rectangle(image, (l, t), (r, b), (255, 255, 0), self.rect_thickness)
                print(f"Confidence: {confidence}")

        processed_image_path = os.path.join(self.processed_folder, filename)
        cv2.imwrite(processed_image_path, image)
        return processed_image_path