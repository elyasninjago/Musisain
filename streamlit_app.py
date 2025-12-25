import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import yt_dlp
import os

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Spatisiify Direct", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; } @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }</style>", unsafe_allow_html=True)

# دریافت کلیدها
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error("تنظیمات اولیه مشکل دارد.")

def download_audio(track_name, artist_name):
    search_query = f"{track_name} {artist_name} audio"
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'song.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{search_query}"])
    return "song.mp3"

st.title("Spatisiify 🎧")
user_input = st.text_input("مودِ الانِت رو بگو:", placeholder="🕺🔥")

if st.button("پیدا کردن و آماده‌سازی موزیک ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو و آماده‌سازی فایل...'):
                prompt = f"Give me ONLY 2 english keywords for: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    
                    # دانلود مخفی در سرور
                    file_path = download_audio(track['name'], track['artists'][0]['name'])
                    
                    # دکمه دانلود مستقیم فایل از سایت خودت
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="📥 دانلود مستقیم فایل MP3",
                            data=file,
                            file_name=f"{track['name']}.mp3",
                            mime="audio/mpeg"
                        )
                    os.remove(file_path) # پاک کردن فایل برای اشغال نشدن فضا
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"مشکلی پیش آمد: {e}")