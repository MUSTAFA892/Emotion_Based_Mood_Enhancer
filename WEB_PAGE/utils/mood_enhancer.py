import os
from google import genai
import json

# Initialize Gemini API client
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
client = genai.Client(api_key=API_KEY)

def get_mood_enhancement(emotion):
    """
    Get fully dynamic content to enhance mood based on detected emotion using Gemini API.
    
    Args:
        emotion: Detected emotion (sad, angry, fear, disgust, neutral, happy, surprise)
        
    Returns:
        dict: Various mood-enhancing content
    """
    try:
        # Construct prompt for Gemini based on emotion
        prompt_ = f"""
        The user's facial expression shows they're feeling {emotion}. As an AI assistant, I want to provide 
        appropriate content to either enhance their mood (if negative) or sustain it (if positive).

        Please create a personalized response based on their emotion ({emotion}) that includes:

        1. A brief personalized message addressing their current emotional state.
        2. A joke that would be most appropriate for someone feeling {emotion}.
        3. An inspirational or fitting quote for their emotional state.
        4. A suggestion for a specific YouTube video (provide the full URL) that would be perfect for someone feeling {emotion}.
        5. A recommended activity they could do right now to either improve or maintain their emotional state.
        6. A helpful tip related to emotional well-being that's relevant to their current emotion.

        Return your response in this exact JSON format:
        {{
            "message": "your personalized message here",
            "joke": "your carefully selected joke here",
            "quote": "your chosen quote here",
            "video_link": "specific youtube link here",
            "activity": "your recommended activity here",
            "wellbeing_tip": "your emotional wellbeing tip here"
        }}
        """
        
        # Call Gemini API to generate dynamic content
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Ensure you're using the correct model identifier
            contents=prompt_  # Use 'contents' instead of 'prompt'
        )

        # Print the raw response for debugging
        print(f"Gemini API Response: {response.text}")

        # Extract and parse the response
        try:
            # Check if the response contains the JSON structure
            content_text = response.text
            start_index = content_text.find('{')
            end_index = content_text.rfind('}') + 1
            
            if start_index >= 0 and end_index > start_index:
                json_text = content_text[start_index:end_index]
                content = json.loads(json_text)
                return content
            else:
                raise ValueError("Could not find valid JSON in the response")
        except Exception as json_error:
            print(f"Error parsing Gemini response: {str(json_error)}")
            print(f"Raw response: {response.text}")
            
            # Fallback logic if parsing fails
            dynamic_fallback = {
                'message': f"I noticed you're feeling {emotion}. Let me try to help with that.",
                'joke': "Why don't scientists trust atoms? Because they make up everything!",
                'quote': "The best way to predict the future is to create it.",
                'video_link': "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
                'activity': "Take a short walk outside to refresh your mind.",
                'wellbeing_tip': "Take a deep breath and try to stay calm."
            }
            return dynamic_fallback

    except Exception as e:
        print(f"Error with Gemini API: {str(e)}")
        # Return fallback content
        dynamic_fallback = {
            'message': f"I noticed you're feeling {emotion}. Let me try to help with that.",
            'joke': "Why don't scientists trust atoms? Because they make up everything!",
            'quote': "The best way to predict the future is to create it.",
            'video_link': "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
            'activity': "Take a short walk outside to refresh your mind.",
            'wellbeing_tip': "Take a deep breath and try to stay calm."
        }
        return dynamic_fallback
