import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- ظاهر متحرک ---
st.set_page_config(page_title="Spatisiify Fixed", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; } @keyframes move { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }</style>", unsafe_allow_html=True)

try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_to_use = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        model = genai.GenerativeModel(model_to_use)
    else:
        st.error("کلید در Secrets پیدا نشد!")
        st.stop()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطای سیستمی: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار اینجا:", placeholder="😎🔥🎸")

if st.button("کشف آهنگ جدید ✨"):
    if user_input:
        try:
            with st.spinner('در حال جادو...'):
                # دستور بسیار سخت‌گیرانه به جمینای برای جلوگیری از پرحرفی
                prompt = f"Give me ONLY 2 english words for a spotify search for these emojis: {user_input}. NO intro, NO explanation, NO extra text."
                response = model.generate_content(prompt)
                
                # محدود کردن دستی متن برای اطمینان از زیر ۲۵۰ کاراکتر
                keywords = response.text.strip()[:50] 
                
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    st.balloons()
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")
                    st.link_button("📥 دانلود/شنیدن", f"https://spotifydown.com/?link={track['external_urls']['spotify']}")
                else:
                    st.warning(f"با کلمات '{keywords}' آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"ارور: {e}")
    else:
        st.toast("ایموجی یادت رفت!")