import streamlit as st
import requests

# Function to call the backend API
def get_playlists(text):
    response = requests.post('http://localhost:5000/get_playlist', json={'text': text})
    return response.json()

# Streamlit app layout
st.set_page_config(page_title="Emotion Music Player", page_icon=":musical_note:", layout="wide")

# Page header
st.title("🎵 Emotion Music Player")
st.write("Discover playlists tailored to your mood or feeling. Enter your mood or feeling below to get started!")

# Styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6F61;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF3D2A;
    }
    .stTextInput>div>input {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #FF6F61;
        width: 100%;
    }
    .stTextInput>div>input:focus {
        border-color: #FF3D2A;
    }
    .playlist {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f9f9f9;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .playlist h3 {
        color: #FF6F61;
    }
    .playlist p {
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Input field for user text
user_input = st.text_input("Enter your mood or feeling...")

# Button to fetch playlists
if st.button("Get Playlist"):
    if user_input:
        # Fetch playlists based on user input
        data = get_playlists(user_input)
        if 'error' in data:
            st.error(f"Error: {data['error']}")
        else:
            st.subheader("Recommended Playlists:")
            for playlist in data.get('playlists', []):
                st.markdown(f"""
                    <div class="playlist">
                        <h3>{playlist['name']}</h3>
                        <p>{playlist.get('description', 'No description available.')}</p>
                        <a href="{playlist['link']}" target="_blank">
                            <button>Listen to Playlist</button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to get recommendations.")
