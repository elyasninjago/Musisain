import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from youtubesearchpython import VideosSearch
import yt_dlp
import os

# ظاهر برنامه
st.set_page_config(page_title="Spatisiify Ultra", page_icon="🎧")
st.markdown("<style>.stApp { background: linear-gradient(135deg, #1db954, #191414); color: white; }</style>", unsafe_allow_html=True)

# تنظیمات مدل هوشمند
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except:
    st.error("خطا در بارگذاری سرویس‌ها")

def get_best_link(query):
    # جستجوی لینک ویدیو به سبک کتابخانه‌های جاوا اسکریپتی (سریع و مخفی)
    videosSearch = VideosSearch(query, limit = 1)
    result = videosSearch.result()
    if result['result']:
        return result['result'][0]['link']
    return None

st.title("Spatisiify Ultra 🎧")
user_input = st.text_input("ایموجی یا اسم آهنگ:", placeholder="🔥 Blinding Lights")

if st.button("شکار موزیک و دانلود مستقیم 🚀"):
    if user_input:
        try:
            with st.spinner('در حال جستجوی هوشمند در دیتابیس‌های جهانی...'):
                res = model.generate_content(f"Give me 2 keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                results = sp.search(q=keywords, limit=1)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    
                    st.image(track['album']['images'][0]['url'], width=200)
                    st.subheader(f"{track_name} - {artist_name}")

                    # پیدا کردن بهترین لینک یوتیوب بدون بلاک شدن
                    video_link = get_best_link(f"{track_name} {artist_name} audio")
                    
                    if video_link:
                        # استفاده از سایت‌های تبدیل‌کننده مستقیم برای فرار از ارور 403
                        # این متد کاربر را به یک صفحه دانلود مستقیم و تمیز می‌برد
                        dl_link = f"https://api.vevioz.com/api/button/mp3/{video_link.split('=')[1]}"
                        
                        st.markdown(f"""
                            <div style="background: #ffffff22; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #1db954;">
                                <p>فایل با بهترین کیفیت آماده است!</p>
                                <a href="{dl_link}" target="_blank" style="text-decoration: none;">
                                    <button style="width: 100%; background: #1db954; color: white; padding: 15px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer;">
                                        📥 دانلود مستقیم MP3 (بدون ارور)
                                    </button>
                                </a>
                                <p style="font-size: 10px; margin-top: 10px; color: #aaa;">بعد از کلیک، چند لحظه صبر کنید تا فایل آماده دانلود شود.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("لینک دانلودی پیدا نشد.")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطا: {e}")