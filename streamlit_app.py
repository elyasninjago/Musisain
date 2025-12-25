import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- دکور و انیمیشن متحرک ---
st.set_page_config(page_title="Spatisiify", page_icon="🎧")
st.markdown("""
    <style>
    @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954);
        background-size: 400% 400%;
        animation: move 10s ease infinite;
    }
    .glass {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px); color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# دریافت کلید از مخفیگاه (Secrets)
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    # استفاده از پایدارترین نام مدل برای جلوگیری از ارور 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطا در تنظیمات امنیتی: کلید پیدا نشد یا اشتباه است.")
    st.stop()

# Spotify - این‌ها فعلاً امن هستند
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

st.title("Spatisiify 🎧")

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    user_input = st.text_input("مودِ الانِت رو با ایموجی بگو:", placeholder="😎🔥🎸")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("کشف آهنگ جدید ✨"):
    if user_input:
        try:
            with st.spinner('هوش مصنوعی در حال تحلیل حس شما...'):
                # گرفتن کلمات کلیدی از جمینای
                prompt = f"Give me ONLY 2 english keywords for a music search based on these emojis: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()
                
                # سرچ در اسپاتیفای
                auth = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
                sp = spotipy.Spotify(auth_manager=auth)
                results = sp.search(q=keywords, limit=10)
                
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    st.markdown("---")
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    if track['preview_url']:
                        st.audio(track['preview_url'])
                    
                    st.link_button("📥 دانلود/شنیدن کامل", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
                else:
                    st.warning("آهنگی پیدا نشد، دوباره امتحان کن.")
        except Exception as e:
            st.error("ارتباط برقرار نشد. احتمالاً کلید API شما هنوز فعال نشده است.")
    else:
        st.toast("اول چند تا ایموجی بذار!")