import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- استایل متحرک و شیک ---
st.set_page_config(page_title="Spatisiify Ultra", page_icon="🎧")
st.markdown("""
    <style>
    @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954);
        background-size: 400% 400%;
        animation: move 10s ease infinite;
        color: white;
    }
    .glass {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# API Keys
API_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

genai.configure(api_key=API_KEY)

# --- تابع هوشمند برای پیدا کردن مدل سالم ---
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # اولویت‌ها
    priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
    for p in priorities:
        if p in available_models:
            return genai.GenerativeModel(p)
    # اگر هیچکدام نبود، اولین مدل لیست را بردار
    return genai.GenerativeModel(available_models[0])

st.title("Spatisiify 🎧")

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    user_input = st.text_input("ایموجی‌هاتو اینجا بذار:", placeholder="🕺✨🎸")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("کشف آهنگ جدید ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجوی جادویی...'):
                # انتخاب هوشمند مدل برای فرار از 404
                model = get_working_model()
                
                prompt = f"Give me 2 english keywords for a music search based on: {user_input}. Just keywords."
                response = model.generate_content(prompt)
                keywords = response.text.strip()
                
                # اسپاتیفای
                auth = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
                sp = spotipy.Spotify(auth_manager=auth)
                
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    st.markdown("---")
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.image(track['album']['images'][0]['url'])
                    with c2:
                        st.subheader(track['name'])
                        st.write(f"🎤 {track['artists'][0]['name']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                    
                    st.link_button("📥 دانلود/شنیدن", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطا: {e}")
            st.info("یک بار دیگر دکمه را بزنید؛ احتمالاً مشکل لحظه‌ای شبکه است.")
    else:
        st.toast("ایموجی بذار!")