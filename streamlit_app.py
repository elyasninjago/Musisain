import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- ظاهر برنامه با پس‌زمینه متحرک ---
st.set_page_config(page_title="Spatisiify Final", page_icon="🎧")

st.markdown("""
    <style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 60px;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white; font-weight: bold; border: none; font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# اعتبارنامه‌ها
API_KEY = "AIzaSyCpNTVQU620tLGOdeFf9QBSk6Pg_o89ZZk"
SPOTIPY_ID = "51666862f91b4a6e9e296d9582847404"
SPOTIPY_SECRET = "a562c839bb9a4567913c0a0989cbd46b"

# پیکربندی مدل
genai.configure(api_key=API_KEY)
# تغییر اصلی اینجاست: استفاده از نسخه 1.5 فلش که ارور 404 نمی‌دهد
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Spatisiify 🎧")
st.write("ایموجی‌هاتو بذار تا بهت بگم چه آهنگی گوش بدی!")

with st.container():
    st.markdown('<div class="glass-effect">', unsafe_allow_html=True)
    user_emojis = st.text_input("مودِ الانت چیه؟", placeholder="مثلا: 🕺🔥🎸")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("پیدا کردن جادوی موسیقی ✨"):
    if user_emojis:
        try:
            with st.spinner('جمینای داره حس ایموجی‌هاتو تحلیل می‌کنه...'):
                prompt = f"Based on these emojis '{user_emojis}', suggest 2 English keywords for a Spotify search. ONLY keywords."
                response = model.generate_content(user_emojis) # ارسال مستقیم برای پایداری بیشتر
                keywords = response.text.strip()
                
                # اتصال به اسپاتیفای
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
                        st.write(f"👤 خواننده: {track['artists'][0]['name']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                    
                    st.link_button("📥 لینک دانلود/شنیدن", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
                else:
                    st.warning("آهنگی پیدا نشد، دوباره تلاش کن.")
        except Exception as e:
            st.error(f"خطا: {e}")
            st.info("راهنمایی: اگر ارور 404 دارید، احتمالاً مدل در این لحظه در دسترس نیست.")
    else:
        st.toast("ایموجی یادت رفت!")