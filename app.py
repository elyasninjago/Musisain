import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from PIL import Image

# --- تنظیمات صفحه ---
st.set_page_config(page_title="Sticker Music", page_icon="🎵", layout="centered")

# --- استایل مخصوص موبایل ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .stButton>button {
        width: 100%; border-radius: 20px; height: 50px;
        background-color: #1DB954; color: white; font-size: 18px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- کلیدهای شما (جایگذاری شده) ---
GENAI_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

# اتصال به سرویس‌ها
try:
    genai.configure(api_key=GENAI_KEY)
    # استفاده از مدل جدید طبق عکس شما
    model = genai.GenerativeModel('gemini-2.5-flash')

    auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error(f"Error in connection: {e}")

st.title("Spatisiify 🎧")
st.write("یک عکس بده، آهنگ تحویل بگیر!")

# آپلود فایل
uploaded_file = st.file_uploader("انتخاب عکس...", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    if st.button("پیدا کردن آهنگ 🎵"):
        with st.spinner('در حال تحلیل...'):
            try:
                # تحلیل عکس
                prompt = "Analyze the mood of this image and give me 2 English keywords for a song search. Just the keywords."
                response = model.generate_content([prompt, img])
                keywords = response.text.strip()
                
                # جستجو در اسپاتیفای
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    
                    st.success(f"آهنگ پیشنهادی برای مود: {keywords}")
                    st.markdown("---")
                    st.subheader(track['name'])
                    st.write(track['artists'][0]['name'])
                    st.image(track['album']['images'][0]['url'])
                    
                    if track['preview_url']:
                        st.audio(track['preview_url'])
                    
                    # لینک دانلود
                    dl_link = f"https://spotifydown.com/?link={track['external_urls']['spotify']}"
                    st.link_button("📥 دانلود رایگان", dl_link)
                else:
                    st.warning("آهنگی پیدا نشد! دوباره تلاش کن.")
            except Exception as e:
                st.error(f"خطا: {e}")