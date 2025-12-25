import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# ظاهر شیک و متحرک
st.set_page_config(page_title="Spatisiify Pro", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # انتخاب خودکار مدل برای فرار از 404
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("لطفاً کلید GEMINI_KEY را در بخش Secrets وارد کنید.")
        st.stop()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطای سیستمی: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار اینجا:", placeholder="🕺🔥🎸")

if st.button("کشف جادوی موسیقی ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو...'):
                prompt = f"Give me ONLY 2 english keywords for a music search based on: {user_input}. No extra text."
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    track_url = track['external_urls']['spotify']
                    
                    st.balloons()
                    st.markdown("---")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.image(track['album']['images'][0]['url'], use_container_width=True)
                    with col2:
                        st.subheader(track['name'])
                        st.write(f"🎤 Artist: {track['artists'][0]['name']}")
                        
                        # پخش آنلاین در صورت وجود
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                        else:
                            st.info("پیش‌نمایش کوتاه موجود نیست.")

                    st.markdown("### 📥 دریافت فایل کامل:")
                    
                    # دکمه دانلود از سایت کمکی (سریع و بدون ارور سرور)
                    st.link_button("🚀 دریافت لینک دانلود MP3", f"https://spotifydown.com/?link={track_url}")
                    
                    # دکمه تلگرام برای دانلود راحت‌تر
                    st.link_button("✈️ ارسال به بات تلگرام (دانلود سریع)", f"https://t.me/SpotifySaveBot?start={track_url}")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error("یه مشکلی پیش اومد، دوباره دکمه رو بزن!")
    else:
        st.toast("اول ایموجی بذار!")