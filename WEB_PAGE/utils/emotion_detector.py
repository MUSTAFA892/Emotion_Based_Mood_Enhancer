import cv2
from deepface import DeepFace

def detect_emotion(frame):
    """
    Detect emotion in the given frame using DeepFace
    
    Args:
        frame: OpenCV image/frame
        
    Returns:
        tuple: (dominant_emotion, confidence)
    """
    try:
        # Convert to RGB (DeepFace expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # If no faces detected, return neutral
        if len(faces) == 0:
            return "neutral", 0
        
        # Get the largest face
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Crop the face
        face_img = rgb_frame[y:y+h, x:x+w]
        
        # Analyze emotion
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
        
        # Extract dominant emotion and its confidence
        dominant_emotion = result[0]["dominant_emotion"]
        emotion_scores = result[0]["emotion"]
        confidence = emotion_scores[dominant_emotion]
        
        # Convert confidence to a standard Python float (to avoid float32 serialization issue)
        return dominant_emotion, float(confidence)  # Convert to standard float
        
    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return "unknown", 0
