# Emotion Detection & Mood Enhancement Flask App

This Flask application detects a user's emotion via webcam using DeepFace and provides mood-enhancing content based on the detected emotion.

## Features

- Real-time emotion detection through webcam
- AI-powered mood enhancement using Google's Gemini API
- Provides jokes, quotes, and YouTube videos to improve mood
- Clean, responsive user interface
- Fallback content if API is unavailable

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/emotion-flask-app.git
   cd emotion-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Gemini API key:
   - Get an API key from https://aistudio.google.com/
   - Set it as an environment variable:
     ```
     export GEMINI_API_KEY="your_api_key_here"  # On Windows: set GEMINI_API_KEY=your_api_key_here
     ```
   - Or update the key in `utils/mood_enhancer.py`

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Allow camera access when prompted
4. Click "Detect Emotion" to analyze your current emotion
5. Click "Enhance My Mood" to receive personalized content based on your emotion

## How It Works

1. The app captures an image from your webcam
2. DeepFace analyzes the image to detect your emotion
3. If you appear sad, angry, fearful, disgusted, or neutral:
   - The Gemini API generates personalized mood-enhancing content
   - You receive a supportive message, joke, quote, and YouTube video
4. If you appear happy or surprised:
   - The app acknowledges your positive mood

## Folder Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates
  - `index.html`: Main page with webcam
  - `result.html`: Results page with mood enhancers
- `static/`: Static files
  - `css/style.css`: CSS styles
  - `js/webcam.js`: JavaScript for webcam handling
- `utils/`: Utility modules
  - `emotion_detector.py`: DeepFace emotion detection
  - `mood_enhancer.py`: Gemini API integration

## Requirements

- Python 3.8+
- Flask
- OpenCV
- DeepFace
- Google Generative AI
- Modern web browser with webcam access

## License

MIT
