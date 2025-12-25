import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- تنظیمات صفحه و انیمیشن پس‌زمینه ---
st.set_page_config(page_title="Spatisiify Emoji", page_icon="🎧", layout="centered")

st.markdown("""
    <style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    .emoji-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 60px;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        font-weight: bold;
        font-size: 22px;
        border: none;
        transition: 0.5s;
    }
    
    .stButton>button:hover {
        letter-spacing: 2px;
        box-shadow: 0 0 20px #1DB954;
    }

    input {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid #1DB954 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- کلیدهای شما ---
GENAI_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

genai.configure(api_key=GENAI_KEY)
# اصلاح نام مدل برای رفع ارور 404
model = genai.GenerativeModel('gemini-pro') 

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- بدنه برنامه ---
st.markdown("<h1 style='text-align: center;'>Spatisiify 🎧</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>ایموجی‌هاتو بفرست، موزیکتو بگیر!</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="emoji-card">', unsafe_allow_html=True)
    user_emojis = st.text_input("مودِ الانِت چیه؟", placeholder="مثلا: 🧊💎🥶")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # فاصله

if st.button("کشف آهنگ جدید ✨"):
    if user_emojis:
        with st.spinner('در حال تحلیل حس ایموجی‌ها توسط هوش مصنوعی...'):
            try:
                # تحلیل ایموجی
                prompt = f"Analyze these emojis '{user_emojis}' and give me only 2 english keywords for a music search. example: 'chill lo-fi' or 'hard rock'"
                response = model.generate_content(prompt)
                search_query = response.text.strip()
                
                # سرچ در اسپاتیفای
                results = sp.search(q=search_query, limit=10, type='track')
                
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    
                    st.markdown("---")
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.image(track['album']['images'][0]['url'])
                    with c2:
                        st.subheader(track['name'])
                        st.write(f"خواننده: {track['artists'][0]['name']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                    
                    dl_link = f"https://spotifydown.com/?link={track['external_urls']['spotify']}"
                    st.link_button(f"📥 دانلود آهنگ", dl_link)
                else:
                    st.warning("آهنگی پیدا نشد.")
            except Exception as e:
                # نمایش ارور به زبان ساده‌تر
                st.error(f"خطا در ارتباط با هوش مصنوعی. لطفا دوباره تلاش کنید.")
                st.info("نکته: مطمئن شوید ایموجی وارد کرده‌اید.")
    else:
        st.toast("لطفا اول ایموجی وارد کن!")

st.markdown("<br><p style='text-align: center; font-size: 10px; opacity: 0.5;'>Made with ❤️ for Musisain</p>", unsafe_allow_html=True)