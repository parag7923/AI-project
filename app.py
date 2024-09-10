import os
import random
from flask import Flask, request, jsonify
from transformers import pipeline
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize CORS
CORS(app)

# Emotion detection setup using Hugging Face model
emotion_detector = pipeline('sentiment-analysis', model='bhadresh-savani/distilbert-base-uncased-finetuned-emotion')

# Spotify API credentials
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Spotify authentication
auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to detect emotion using Hugging Face model
def detect_emotion(text):
    try:
        response = emotion_detector(text)
        emotion = response[0]['label'].lower()
        return emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return "unknown"

# Function to search for Spotify playlists based on a emotion tags
def find_playlists_for_keyword(keyword, limit=10):
    try:
        # Generate random queries to get diverse playlists
        random_queries = [f"{keyword} playlist", f"best {keyword} playlists", f"{keyword} hits"]
        query = random.choice(random_queries)
        results = sp.search(q=query, type='playlist', limit=limit)
        playlists = results['playlists']['items']
        return [{
            'name': playlist['name'],
            'description': playlist['description'],
            'link': playlist['external_urls']['spotify']
        } for playlist in playlists]
    except Exception as e:
        print(f"Error finding playlists: {e}")
        return []

# Function to find playlists based on emotion
def find_playlists_for_emotion(emotion, limit=10):
    emotion_to_query = {
    "joy": "happy",
    "anger": "angry",
    "fear": "fearful",
    "sadness": "sad",
    "surprise": "surprised",
    "disgust": "disgusted",
    "trust": "trusting",
    "anticipation": "anticipating",
    "sadness": "melancholic",
    "boredom": "bored",
    "frustration": "frustrated",
    "confusion": "confused",
    "excitement": "excited",
    "contentment": "content",
    "relief": "relieved",
    "nostalgia": "nostalgic",
    "pride": "proud",
    "guilt": "guilty",
    "shame": "ashamed",
    "embarrassment": "embarrassed",
    "hope": "hopeful",
    "unknown": "mood",
    "mixed": "mixed emotions",
    "indifference": "indifferent"
    }

    query = emotion_to_query.get(emotion, "mood")
    
    try:
        # Generate random queries to get diverse playlists
        random_queries = [f"{query} playlist", f"best {query} playlists", f"{query} hits"]
        query = random.choice(random_queries)
        results = sp.search(q=query, type='playlist', limit=limit)
        playlists = results['playlists']['items']
        return [{
            'name': playlist['name'],
            'description': playlist['description'],
            'link': playlist['external_urls']['spotify']
        } for playlist in playlists]
    except Exception as e:
        print(f"Error finding playlists: {e}")
        return []

@app.route('/get_playlist', methods=['POST'])
def get_playlist():
    data = request.json
    user_text = data.get('text', '')

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Detect emotion from the text
    emotion = detect_emotion(user_text)
    
    # Find playlists based on emotion and keyword
    emotion_playlists = find_playlists_for_emotion(emotion)
    keyword_playlists = find_playlists_for_keyword(user_text)

    # Combine and randomize the playlists
    all_playlists = emotion_playlists + keyword_playlists
    random.shuffle(all_playlists)
    
    # Select up to 4 playlists
    selected_playlists = all_playlists[:4]

    return jsonify({
        "playlists": selected_playlists
    })

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
