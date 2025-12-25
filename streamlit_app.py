import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- ظاهر برنامه ---
st.set_page_config(page_title="Spatisiify Fixed Link", page_icon="🎧")
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

                    st.markdown("### 📥 بخش دانلود (اصلاح شده):")
                    
                    # لینک درست شده با r آخر!
                    final_dl_url = f"https://spotidownloader.com/download?link={track_url}"
                    
                    st.markdown(f"""
                        <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; border: 1px solid #1DB954;">
                            <p style="color: #FFD700; font-size: 14px;">نکته: برای اینکه اپلیکیشن اسپاتیفای باز نشود، روی دکمه زیر نگه دارید و <b>Open in New Tab</b> را بزنید.</p>
                            <a href="{final_dl_url}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background-color: #1DB954; color: white; padding: 15px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; font-size: 16px;">
                                    📥 ورود به صفحه دانلود MP3
                                </button>
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    st.text_input("لینک مستقیم برای کپی:", track_url)
                    st.link_button("✈️ ارسال به تلگرام", f"https://t.me/SpotifySaveBot?start={track_url}")
                    
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error("یه بار دیگه بزن روی دکمه!")
    else:
        st.toast("ایموجی یادت نره!")
    