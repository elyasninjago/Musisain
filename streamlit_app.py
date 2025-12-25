import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import yt_dlp
import os

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify Ultra", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات اتصال
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        
        # --- بخش هوشمند برای فرار از 404 ---
        # لیست مدل‌های در دسترس اکانت شما را می‌گیرد
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # انتخاب اولین مدل معتبر (معمولاً gemini-pro یا 1.5-flash)
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("لطفاً GEMINI_KEY را در Secrets ست کنید.")
        st.stop()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطای سیستمی در شروع: {e}")

def download_audio(track_name, artist_name):
    search_query = f"{track_name} {artist_name} official audio"
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
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
user_input = st.text_input("ایموجی‌هاتو بذار:", placeholder="🕺🔥")

if st.button("پیدا کردن و آماده‌سازی فایل ✨"):
    if user_input:
        try:
            with st.spinner('هوش مصنوعی در حال جستجوی آهنگ و آماده‌سازی فایل دانلود...'):
                prompt = f"Give me ONLY 2 keywords for: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    
                    # دانلود مستقیم در سرور
                    file_path = download_audio(track['name'], track['artists'][0]['name'])
                    
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="📥 دانلود مستقیم فایل MP3 (بدون خروج از سایت)",
                            data=file,
                            file_name=f"{track['name']}.mp3",
                            mime="audio/mpeg"
                        )
                    os.remove(file_path)
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"ارور: {e}")
    else:
        st.toast("ایموجی بذار!")