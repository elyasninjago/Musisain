import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import traceback

# --- تنظیمات ظاهر و انیمیشن ---
st.set_page_config(page_title="Spatisiify Debug Mode", page_icon="🎧")

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
    }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 60px;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- بخش دیباگ در حافظه ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(message):
    st.session_state.logs.append(message)

# --- تنظیمات API ---
GENAI_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

# --- شروع فرآیند ---
st.title("Spatisiify 🎧")

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    user_input = st.text_input("ایموجی‌های مودِ الانت رو بذار:", placeholder="🎯🔥🎸")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("کشف آهنگ جدید ✨"):
    if user_input:
        add_log(f"Starting process for: {user_input}")
        try:
            # ۱. تنظیم گوگل
            add_log("Configuring Gemini...")
            genai.configure(api_key=GENAI_KEY)
            # استفاده از مدل با نام کامل برای جلوگیری از 404
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            
            # ۲. تحلیل حس
            add_log("Asking Gemini for keywords...")
            prompt = f"Give me ONLY 2 english keywords for a spotify search based on these emojis: {user_input}. No extra text."
            response = model.generate_content(prompt)
            keywords = response.text.strip()
            add_log(f"Gemini returned: {keywords}")
            
            # ۳. اسپاتیفای
            add_log("Connecting to Spotify...")
            auth = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
            sp = spotipy.Spotify(auth_manager=auth)
            
            results = sp.search(q=keywords, limit=10)
            if results['tracks']['items']:
                track = random.choice(results['tracks']['items'])
                add_log(f"Found track: {track['name']}")
                
                st.balloons()
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(track['album']['images'][0]['url'])
                with col2:
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    if track['preview_url']:
                        st.audio(track['preview_url'])
                
                st.link_button("📥 دانلود آهنگ", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
            else:
                add_log("No tracks found on Spotify.")
                st.warning("آهنگی پیدا نشد.")
                
        except Exception as e:
            error_details = traceback.format_exc()
            add_log(f"CRITICAL ERROR: {str(e)}")
            add_log(error_details)
            st.error(f"خطا رخ داد. لطفا بخش Debug Log پایین صفحه را چک کنید.")
    else:
        st.toast("ایموجی کو؟")

# --- نمایش لاگ‌ها برای دیباگ ---
st.write("---")
with st.expander("🛠 بخش دیباگ (Debug Log)"):
    if st.session_state.logs:
        for log in st.session_state.logs:
            st.code(log)
    else:
        st.write("هنوز عملیاتی انجام نشده.")

if st.button("پاک کردن لاگ‌ها"):
    st.session_state.logs = []
    st.rerun()