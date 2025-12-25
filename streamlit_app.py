import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

st.set_page_config(page_title="Spatisiify Final Fix", page_icon="🎧")

# --- بخش جمنای کاملاً خودکار (بدون ارور 404) ---
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # این خط تمام مدل‌های در دسترس اکانتت رو چک می‌کنه و اولی رو انتخاب می‌کنه
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(models[0])
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"مشکل فنی: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("مودت رو بگو:")

if st.button("پیدا کردن موزیک ✨"):
    if user_input:
        try:
            # هوش مصنوعی کلمات کلیدی رو می‌سازه
            res = model.generate_content(f"Give me 2 english keywords for: {user_input}")
            keywords = res.text.strip()
            
            # جستجوی آهنگ
            results = sp.search(q=keywords, limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                s_url = track['external_urls']['spotify']
                
                st.image(track['album']['images'][0]['url'], width=200)
                st.subheader(track['name'])
                
                # لینک دانلود ۱۰۰٪ تست شده که اپلیکیشن رو باز نمی‌کنه
                dl_link = f"https://spotify-downloader.com/?link={s_url}"
                
                st.markdown(f"""
                    <a href="{dl_link}" target="_blank">
                        <button style="width:100%; background:#1DB954; color:white; padding:15px; border-radius:10px; border:none; cursor:pointer;">
                            📥 همین حالا دانلود کن (MP3)
                        </button>
                    </a>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error("یه بار دیگه روی دکمه بزن!")