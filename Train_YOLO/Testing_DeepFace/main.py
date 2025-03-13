import cv2
from deepface import DeepFace

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    print("Press 'q' to capture an image and analyze emotion.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert the frame to grayscale (Haar Cascade works with grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Loop over each detected face
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Crop the face region from the frame
            face_region = frame[y:y + h, x:x + w]

            # Perform emotion analysis on the face
            result = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)

            # Extract the dominant emotion
            dominant_emotion = result[0]["dominant_emotion"]

            # Display the emotion text on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f'{dominant_emotion}', (x, y - 10), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame with the face and emotion
        cv2.imshow('Webcam - Press q to capture', frame)

        # Wait for the user to press 'q' to capture and analyze emotion
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Press 'q' to capture and analyze
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
