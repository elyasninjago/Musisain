import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- ظاهر برنامه ---
st.set_page_config(page_title="Spatisiify Express", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # پیدا کردن خودکار مدل فعال برای جلوگیری از ارور 404
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("کلید Gemini تنظیم نشده است.")
        st.stop()
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطای سیستمی: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("مودِت رو با ایموجی بگو:", placeholder="🔥😎")

if st.button("کشف و دانلود سریع ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجوی بهترین آهنگ...'):
                res = model.generate_content(f"Give me ONLY 2 english keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=5)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    s_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=250)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")

                    st.markdown("---")
                    st.markdown("### 📥 روش‌های دانلود فوق‌سریع:")

                    # دکمه ۱: بات تلگرام (بهترین و سریع‌ترین گزینه برای موبایل)
                    tg_url = f"https://t.me/SpotifySaveBot?start={s_url}"
                    st.markdown(f"""
                        <a href="{tg_url}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #0088cc; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; margin-bottom: 10px;">
                                ✈️ دانلود از تلگرام (ارسال فایل MP3)
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

                    # دکمه ۲: معتبرترین سایت دانلودر فعلی (SpotifyDown)
                    sd_url = f"https://spotifydown.com/?link={s_url}"
                    st.markdown(f"""
                        <a href="{sd_url}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #1DB954; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold;">
                                🌐 دانلود از سایت مستقیم (MP3)
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

                    st.info("نکته: در سایت SpotifyDown بعد از باز شدن، دکمه Download را بزنید تا فایل آماده شود.")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error("مشکلی پیش آمد، لطفاً دوباره دکمه را بزنید.")
    else:
        st.toast("ایموجی؟")