import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import yt_dlp
import os

# ظاهر شیک
st.set_page_config(page_title="Spatisiify Pro", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات اتصال هوشمند
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("Secrets را چک کنید!")
        st.stop()
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"Error: {e}")

# تابع اصلی دانلود که یوتیوب را دور می‌زند
def download_music(track_name, artist_name):
    query = f"{track_name} {artist_name} lyrics"
    file_path = "music_file.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music_file',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # ترفند دور زدن 403: استفاده از User-Agent مرورگر معمولی
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])
    
    return f"{file_path}"

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار اینجا:", placeholder="🔥😎")

if st.button("کشف و دانلود مستقیم ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو و استخراج فایل (ممکن است ۱ دقیقه طول بکشد)...'):
                res = model.generate_content(f"Give me 2 search keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                
                search_res = sp.search(q=keywords, limit=5)
                if search_res['tracks']['items']:
                    track = random.choice(search_res['tracks']['items'])
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.caption(f"Artist: {track['artists'][0]['name']}")

                    # شروع فرآیند دانلود داخلی
                    try:
                        music_file = download_music(track['name'], track['artists'][0]['name'])
                        
                        with open(music_file, "rb") as f:
                            st.download_button(
                                label="📥 دانلود مستقیم فایل MP3",
                                data=f,
                                file_name=f"{track['name']}.mp3",
                                mime="audio/mpeg"
                            )
                        os.remove(music_file) # پاکسازی سرور
                    except Exception as dl_error:
                        st.error(f"یوتیوب اجازه دانلود مستقیم نداد. از دکمه کمکی استفاده کنید.")
                        st.link_button("✈️ ارسال به بات تلگرام (بدون ارور)", f"https://t.me/SpotifySaveBot?start={track['external_urls']['spotify']}")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error("مشکلی پیش آمد، دوباره تلاش کنید.")
    else:
        st.toast("ایموجی؟")