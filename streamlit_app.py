import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests
import os

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Spatisiify Pro", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات مدل هوشمند
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("کلید Gemini در Secrets یافت نشد!")
        st.stop()
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطای سیستمی: {e}")

# --- تابع جادویی دانلود مستقیم در سرور ---
def download_from_api(spotify_url):
    # استفاده از یک API عمومی برای گرفتن لینک مستقیم فایل
    api_url = f"https://api.spotifydownloader.org/download?link={spotify_url}"
    try:
        response = requests.get(api_url).json()
        if response['success']:
            # دانلود فایل در حافظه موقت سرور
            audio_data = requests.get(response['link']).content
            return audio_data, response['metadata']['name']
    except:
        return None, None

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار:", placeholder="🕺🔥")

if st.button("کشف و دانلود مستقیم فایل ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو و تولید فایل MP3...'):
                res = model.generate_content(f"Only 2 keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    s_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")

                    # عملیات دانلود مستقیم
                    audio_bytes, file_name = download_from_api(s_url)
                    
                    if audio_bytes:
                        st.balloons()
                        # پخش موزیک در خود سایت
                        st.audio(audio_bytes, format="audio/mp3")
                        
                        # دکمه دانلود واقعی فایل
                        st.download_button(
                            label="📥 ذخیره فایل MP3 روی گوشی/کامپیوتر",
                            data=audio_bytes,
                            file_name=f"{file_name}.mp3",
                            mime="audio/mpeg"
                        )
                    else:
                        st.error("متاسفانه سرور دانلود فعلاً پاسخگو نیست. از لینک کمکی استفاده کنید.")
                        st.link_button("🌐 لینک دانلود کمکی", f"https://spotifydown.com/?link={s_url}")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطا: {e}")
    else:
        st.toast("ایموجی یادت نره!")