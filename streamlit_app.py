import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- تنظیمات ظاهر ---
st.set_page_config(page_title="Spatisiify Final Fix", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1DB954); background-size: 400% 400%; animation: move 10s ease infinite; color: white; }</style>", unsafe_allow_html=True)

try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    else:
        st.error("کلید پیدا نشد!")
        st.stop()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except Exception as e:
    st.error(f"خطا: {e}")

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار:", placeholder="🕺🔥")

if st.button("کشف آهنگ ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو...'):
                prompt = f"Give me ONLY 2 keywords for: {user_input}"
                response = model.generate_content(prompt)
                keywords = response.text.strip()[:50]
                
                results = sp.search(q=keywords, limit=10)
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    track_url = track['external_urls']['spotify']
                    
                    st.balloons()
                    st.markdown("---")
                    
                    st.image(track['album']['images'][0]['url'], width=250)
                    st.subheader(f"🎵 {track['name']}")
                    st.write(f"🎤 {track['artists'][0]['name']}")

                    st.markdown("### 📥 دریافت فایل (بدون باز شدن اپلیکیشن):")
                    
                    # --- ترفند جدید برای دور زدن اپلیکیشن اسپاتیفای ---
                    # استفاده از لینک مستقیم تبدیل‌کننده
                    dl_link = f"https://spotifydown.com/?link={track_url}"
                    
                    st.markdown(f"""
                        <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                            <p style="color: #FFD700;">⚠️ اگر با کلیک کردن اپلیکیشن اسپاتیفای باز شد، انگشتت را روی دکمه زیر نگه دار و <b>Open in New Tab</b> را بزن.</p>
                            <a href="{dl_link}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background-color: #1DB954; color: white; padding: 12px; border: none; border-radius: 25px; font-weight: bold; cursor: pointer;">
                                    🚀 ورود به صفحه دانلود MP3
                                </button>
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    # نمایش لینک برای کپی دستی (راه حل احتیاطی)
                    st.text_input("لینک آهنگ برای کپی دستی (اگر دکمه بالا کار نکرد):", track_url)
                    
                    st.link_button("✈️ ارسال به تلگرام (بهترین گزینه)", f"https://t.me/SpotifySaveBot?start={track_url}")
                else:
                    st.warning("پیدا نشد.")
        except Exception as e:
            st.error("دوباره امتحان کن!")
    else:
        st.toast("ایموجی کو؟")