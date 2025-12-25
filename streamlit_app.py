import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# تنظیمات استایل
st.set_page_config(page_title="Spatisiify", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; } @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }</style>", unsafe_allow_html=True)

# اعتبارنامه‌ها
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
    SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(SPOTIPY_ID, SPOTIPY_SECRET))
except Exception as e:
    st.error(f"خطا در بارگذاری کلیدها: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("مودِ الانِت رو با ایموجی بگو:", placeholder="😎🔥🎸")

if st.button("کشف آهنگ جدید ✨"):
    if user_input:
        try:
            with st.spinner('در حال تحلیل...'):
                response = model.generate_content(f"Keywords for spotify based on: {user_input}")
                keywords = response.text.strip()
                
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    st.link_button("📥 دانلود/شنیدن", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
        except Exception as e:
            # اینجا دقیقاً می‌گوید مشکل چیست
            st.error(f"جزئیات خطا: {e}") 
    else:
        st.toast("ایموجی بذار!")