import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify Professional", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات هوش مصنوعی و اسپاتیفای
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("کلید Gemini تنظیم نشده است.")
        st.stop()
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطا در اتصال: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("مودِت رو بگو:", placeholder="🔥😎")

if st.button("کشف و دریافت مستقیم ✨"):
    if user_input:
        try:
            with st.spinner('در حال پیدا کردن بهترین کیفیت...'):
                prompt = f"Give me ONLY 2 keywords for: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    spotify_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track_name)
                    st.write(f"🎤 {artist_name}")

                    # ایجاد دکمه دانلود مستقیم با استفاده از API تبدیل‌کننده
                    # این لینک مستقیم فایل رو برای مرورگر آماده می‌کنه
                    dl_api_url = f"https://api.spotifydownloader.org/download?link={spotify_url}"
                    
                    st.markdown(f"""
                        <div style="background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; border: 2px solid #1DB954; text-align: center;">
                            <h4 style="color: white; margin-bottom: 15px;">فایل شما آماده است!</h4>
                            <a href="https://scdl.to/download?url={spotify_url}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background-color: #1DB954; color: white; padding: 15px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; font-size: 18px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                                    📥 شروع دانلود مستقیم (MP3)
                                </button>
                            </a>
                            <p style="font-size: 12px; margin-top: 10px; color: #ccc;">بدون خروج از سایت، فایل در برگه جدید آماده دانلود می‌شود.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if track['preview_url']:
                        st.audio(track['preview_url'])
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error("سرور شلوغه، یه بار دیگه امتحان کن!")
    else:
        st.toast("ایموجی؟")