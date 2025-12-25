import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- تنظیمات صفحه و انیمیشن پس‌زمینه متحرک ---
st.set_page_config(page_title="Spatisiify Emoji", page_icon="🎧", layout="centered")

st.markdown("""
    <style>
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954);
        background-size: 400% 400%;
        animation: gradientAnimation 12s ease infinite;
        color: white;
    }

    /* کارت شیشه‌ای */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* دکمه درخشان */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 60px;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        font-weight: 800;
        font-size: 22px;
        border: none;
        box-shadow: 0 0 15px rgba(29, 185, 84, 0.4);
        transition: 0.4s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px #1DB954;
    }

    input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- اعتبارنامه‌ها ---
GENAI_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

# پیکربندی هوش مصنوعی با نسخه مدل پایدار
genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# پیکربندی اسپاتیفای
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- طراحی صفحه ---
st.markdown("<h1 style='text-align: center; font-size: 50px;'>Spatisiify 🎧</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>حست رو با ایموجی بگو، بقیه‌اش با من!</p>", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
user_emojis = st.text_input("ایموجی‌های مودِ الانت:", placeholder="مثلا: ✨🌊🧘")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("کشف جادوی موسیقی ✨"):
    if user_emojis:
        with st.spinner('هوش مصنوعی در حال گوش دادن به ایموجی‌ها...'):
            try:
                # تحلیل ایموجی
                prompt = f"Analyze these emojis '{user_emojis}' and suggest a specific music genre or mood. Give me ONLY 2 English keywords for Spotify search."
                response = model.generate_content(prompt)
                search_query = response.text.strip()
                
                # جستجو
                results = sp.search(q=search_query, limit=12, type='track')
                
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    
                    st.markdown("---")
                    col1, col2 = st.columns([1, 1.5])
                    with col1:
                        st.image(track['album']['images'][0]['url'], use_container_width=True)
                    with col2:
                        st.subheader(track['name'])
                        st.write(f"🎤 {track['artists'][0]['name']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                    
                    # دکمه دانلود با استایل
                    dl_url = f"https://spotifydown.com/?link={track['external_urls']['spotify']}"
                    st.link_button("📥 دانلود رایگان آهنگ", dl_url)
                else:
                    st.warning("مود خاصیه! آهنگی براش پیدا نکردم.")
            except Exception as e:
                st.error("ارتباط برقرار نشد. یک بار دیگر امتحان کنید.")
    else:
        st.toast("لطفا اول چند تا ایموجی بذار!")

st.markdown("<br><p style='text-align: center; font-size: 12px; opacity: 0.4;'>Made for a special Musisain ❤</p>", unsafe_allow_html=True)