import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import yt_dlp
import os

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify Pro Downloader", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات اتصال
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("کلید Gemini را در Secrets ست کنید.")
        st.stop()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطا در راه اندازی: {e}")

# تابع اصلی دانلود بدون مسدودی
def download_track(track_name, artist_name):
    search_query = f"{track_name} {artist_name} audio"
    # تنظیمات مخصوص برای دور زدن محدودیت‌های یوتیوب در سرور
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.mp3',
        'quiet': True,
        'no_warnings': True,
        'source_address': '0.0.0.0', # برای جلوگیری از بلاک شدن IP
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{search_query}"])
    return "song.mp3"

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار:", placeholder="🕺🔥")

if st.button("پیدا کردن و دانلود مستقیم ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجوی هوشمند و استخراج فایل MP3...'):
                prompt = f"Give me ONLY 2 keywords for: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    
                    # دانلود در سرور
                    file_name = download_track(track['name'], track['artists'][0]['name'])
                    
                    # ارائه فایل به کاربر برای دانلود مستقیم از خودِ سایت
                    with open(file_name, "rb") as f:
                        st.download_button(
                            label="📥 همین حالا دانلود کن (MP3)",
                            data=f,
                            file_name=f"{track['name']}.mp3",
                            mime="audio/mpeg"
                        )
                    # حذف فایل موقت از سرور
                    if os.path.exists(file_name):
                        os.remove(file_name)
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطا در استخراج: {e}. لطفاً دوباره دکمه را بزنید.")
    else:
        st.toast("ایموجی یادت رفت!")