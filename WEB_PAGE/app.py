from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import time
import base64
import cv2
import numpy as np
from utils.emotion_detector import detect_emotion
from utils.mood_enhancer import get_mood_enhancement

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/detect_emotion', methods=['POST'])
def process_emotion():
    # Get image data from the request
    image_data = request.json.get('image_data', '')
    if not image_data:
        return jsonify({'error': 'No image data received'}), 400
    
    # Remove the data:image/jpeg;base64, prefix
    image_data = image_data.split(',')[1]
    
    # Decode base64 image
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    # Detect emotion using DeepFace
    try:
        emotion, confidence = detect_emotion(frame)
        
        # Store the emotion in session
        session['emotion'] = emotion
        session['confidence'] = confidence
        
        return jsonify({
            'status': 'success',
            'emotion': emotion,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/enhance_mood')
def enhance_mood():
    emotion = session.get('emotion', 'neutral')
    confidence = session.get('confidence', 0)
    
    # Get mood enhancement content based on detected emotion
    # Now we handle all emotions, not just negative ones
    mood_content = get_mood_enhancement(emotion)
    
    return render_template('result.html', 
                          emotion=emotion, 
                          confidence=confidence, 
                          mood_content=mood_content)

if __name__ == '__main__':
    app.run(debug=True)