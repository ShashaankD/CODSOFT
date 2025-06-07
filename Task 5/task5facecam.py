import cv2
import os

# Set the name of the person
person_name = input("Enter your name: ")

# Create full path from the script's current location
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script folder
save_path = os.path.join(base_dir, "train", person_name)

# Create the directory if it doesn't exist
os.makedirs(save_path, exist_ok=True)

# Load Haar cascade face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)
print("📸 Press 'c' to capture face image, 'q' to quit.")

img_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the face
        face_img = frame[y:y + h, x:x + w]

    cv2.imshow("Face Capture", frame)
    key = cv2.waitKey(1)

    if key == ord('c') and len(faces) > 0:
        img_id += 1
        img_filename = f"{img_id}.jpg"
        img_full_path = os.path.join(save_path, img_filename)
        cv2.imwrite(img_full_path, face_img)
        print(f"✔️ Captured and saved {img_full_path}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"📂 Images saved in: {save_path}")
