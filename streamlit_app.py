import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os
import subprocess

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify spotDL", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #121212, #1DB954); color: white; }</style>", unsafe_allow_html=True)

# تنظیمات هوش مصنوعی و اسپاتیفای
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطا در تنظیمات: {e}")

# تابع اصلی با استفاده از دستورات سیستم برای spotdl
def download_with_spotdl(spotify_url):
    try:
        # حذف فایل‌های قبلی برای جلوگیری از تداخل
        for f in os.listdir("."):
            if f.endswith(".mp3"):
                os.remove(f)
        
        # اجرای spotdl از طریق خط فرمان (سیستمی که spotdl با آن کار می‌کند)
        subprocess.check_call(["spotdl", "download", spotify_url])
        
        # پیدا کردن نام فایلی که دانلود شده
        for file in os.listdir("."):
            if file.endswith(".mp3"):
                return file
    except Exception as e:
        return None

st.title("Spatisiify 🎧")
user_input = st.text_input("چه موزیکی می‌خوای؟ (ایموجی یا اسم)", placeholder="💃 Energy")

if st.button("شروع دانلود داخلی با spotDL 🚀"):
    if user_input:
        try:
            with st.spinner('در حال جستجو و دانلود (این روش کمی زمان‌بر اما با کیفیت است)...'):
                res = model.generate_content(f"Only 2 keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                results = sp.search(q=keywords, limit=1)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    s_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.write(f"🎵 **{track['name']}** - {track['artists'][0]['name']}")

                    # اجرای پروسه spotdl
                    file_path = download_with_spotdl(s_url)
                    
                    if file_path and os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 دانلود مستقیم فایل (MP3)",
                                data=f,
                                file_name=file_path,
                                mime="audio/mpeg"
                            )
                        st.success("آهنگ با موفقیت توسط spotDL استخراج شد!")
                        os.remove(file_path) # پاکسازی
                    else:
                        st.error("spotDL نتوانست آهنگ را در منابع آزاد پیدا کند.")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطای سیستمی: {e}")