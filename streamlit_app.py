import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- تنظیمات پیشرفته ظاهر (UI Design) ---
st.set_page_config(page_title="Spatisiify Emoji", page_icon="🎧", layout="centered")

st.markdown("""
    <style>
    /* پس‌زمینه کل صفحه */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    /* استایل کارت‌ها */
    .emoji-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    /* دکمه اصلی اسپاتیفای */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 55px;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        font-weight: bold;
        font-size: 20px;
        border: none;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- اعتبار سنجی ---
GENAI_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- بدنه اصلی برنامه ---
st.title("Spatisiify 🎧")
st.markdown("<p style='text-align: center; color: #b3b3b3;'>ایموجی‌هاتو بفرست، موزیکتو بگیر!</p>", unsafe_allow_html=True)

# کادر دریافت ایموجی
with st.container():
    st.markdown('<div class="emoji-card">', unsafe_allow_html=True)
    user_emojis = st.text_input("ایموجی‌های الانت رو اینجا بذار:", placeholder="مثلا: 🔥🎸😎 یا 🌧️☕💔")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("کشف آهنگ جدید ✨"):
    if user_emojis:
        with st.spinner('در حال خوندن حسِ ایموجی‌ها...'):
            try:
                # تحلیل ایموجی توسط جمینای
                prompt = f"Based on these emojis '{user_emojis}', suggest a music mood or genre. Give me only 2 English keywords for Spotify search. No extra words."
                response = model.generate_content(prompt)
                search_query = response.text.strip()
                
                # جستجو در اسپاتیفای
                results = sp.search(q=search_query, limit=15, type='track')
                
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    
                    # نمایش نتیجه با دکور زیبا
                    st.markdown("---")
                    st.balloons()
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(track['album']['images'][0]['url'], border_radius=15)
                    with col2:
                        st.subheader(track['name'])
                        st.write(f"👤 {track['artists'][0]['name']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                        else:
                            st.info("پیش‌نمایش ندارد، اما از لینک زیر دانلود کن 👇")
                    
                    # دکمه دانلود شیک
                    dl_url = f"https://spotifydown.com/?link={track['external_urls']['spotify']}"
                    st.link_button(f"📥 دانلود آهنگ {track['name']}", dl_url)
                    
                else:
                    st.error("آهنگی متناسب با این حس پیدا نشد.")
            except Exception as e:
                st.error(f"یه مشکلی پیش اومد: {e}")
    else:
        st.warning("اول چند تا ایموجی بذار!")

st.markdown("<br><br><p style='text-align: center; font-size: 12px; color: #666;'>Powerd by Gemini & Spotify</p>", unsafe_allow_html=True)