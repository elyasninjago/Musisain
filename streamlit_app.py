import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import requests

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify Pro", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(to right, #1e1e2f, #1db954); color: white; }</style>", unsafe_allow_html=True)

# تنظیمات مدل و اسپاتیفای
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except:
    st.error("خطا در اتصال به سرویس‌ها")

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی‌هاتو بذار:", placeholder="🕺🔥")

if st.button("پیدا کردن و دانلود مستقیم ✨"):
    if user_input:
        try:
            with st.spinner('در حال آماده‌سازی فایل موزیک...'):
                res = model.generate_content(f"Only 2 keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                results = sp.search(q=keywords, limit=5)
                
                if results['tracks']['items']:
                    track = random.choice(results['tracks']['items'])
                    s_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")

                    # --- تلاش برای دانلود مستقیم از یک دیتابیس متن‌باز ---
                    # ما اینجا به جای یوتیوب، از یک گیت‌وی (Gateway) استفاده می‌کنیم
                    try:
                        # این لینک یک سرور واسطه است که فایل رو میگیره و به پایتون میده
                        gateway_url = f"https://api.spotifydownloader.org/download?link={s_url}"
                        response = requests.get(gateway_url).json()
                        
                        if response['success']:
                            music_data = requests.get(response['link']).content
                            
                            st.audio(music_data, format="audio/mp3")
                            
                            st.download_button(
                                label="📥 ذخیره مستقیم آهنگ (MP3)",
                                data=music_data,
                                file_name=f"{track['name']}.mp3",
                                mime="audio/mpeg"
                            )
                        else:
                            st.error("سرور دانلود مستقیم فعلاً در دسترس نیست.")
                    except:
                        # اگر سرور بالا جواب نداد، از این دکمه هوشمند استفاده کن
                        # این دکمه کاربر رو نمیفرسته تو اسپاتیفای، میبره تو صفحه دانلود
                        st.warning("دانلود مستقیم داخلی با خطا مواجه شد. از این لینک استفاده کن:")
                        st.link_button("🚀 لینک دانلود سریع (بدون نیاز به تلگرام)", f"https://spotify-downloader.com/?link={s_url}")
                else:
                    st.warning("چیزی پیدا نشد.")
        except:
            st.error("دوباره امتحان کن!")