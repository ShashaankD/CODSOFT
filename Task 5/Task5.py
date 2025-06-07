import cv2
import os
import numpy as np

# Initialize recognizer and face detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_images_and_labels(data_folder):
    face_samples = []
    ids = []
    label_map = {}
    current_id = 0

    for person_name in os.listdir(data_folder):
        person_path = os.path.join(data_folder, person_name)
        if not os.path.isdir(person_path):
            continue

        label_map[current_id] = person_name

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            faces = detector.detectMultiScale(gray_img)
            for (x, y, w, h) in faces:
                face_samples.append(gray_img[y:y+h, x:x+w])
                ids.append(current_id)

        current_id += 1

    return face_samples, ids, label_map

# Train recognizer
faces, ids, label_map = get_images_and_labels("train")
recognizer.train(faces, np.array(ids))

# Open webcam
cam = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        name = label_map.get(face_id, "Unknown")
        confidence_text = f"{name} ({round(100 - confidence)}%)"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, confidence_text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.imshow("Live Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
