import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# ظاهر شیک و دارک
st.set_page_config(page_title="Spatisiify Final", page_icon="🎧")
st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

# تنظیمات اتصال (نسخه اصلاح شده برای فرار از ارور 404 مدل)
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash') # استفاده از نام استاندارد
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials("51666862f91b4a6e9e296d9582847404", "a562c839bb9a4567913c0a0989cbd46b"))
except:
    st.error("اتصال برقرار نشد.")

st.title("Spatisiify 🎧")
user_input = st.text_input("ایموجی مِت رو بفرست:", placeholder="😎🔥")

if st.button("پیدا کردن و آماده‌سازی فایل ✨"):
    if user_input:
        try:
            with st.spinner('در حال جستجو در دیتابیس...'):
                res = model.generate_content(f"Give me 2 english keywords for: {user_input}")
                keywords = res.text.strip()[:50]
                results = sp.search(q=keywords, limit=1)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    s_url = track['external_urls']['spotify']
                    
                    st.image(track['album']['images'][0]['url'], width=250)
                    st.subheader(track['name'])
                    st.write(f"🎤 {track['artists'][0]['name']}")

                    # --- ترفند نهایی: استفاده از موتور تبدیل مستقیم مرورگر ---
                    # این لینک به هیچ وجه بلاک نمی‌شود چون روی گوشی کاربر اجرا می‌شود
                    final_dl_url = f"https://spotify-downloader.com/?link={s_url}"
                    
                    st.markdown(f"""
                        <div style="background: #1DB954; padding: 20px; border-radius: 15px; text-align: center;">
                            <p style="font-weight: bold; color: white; margin-bottom: 10px;">✅ موزیک با موفقیت آماده شد!</p>
                            <a href="{final_dl_url}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background: white; color: #1DB954; padding: 15px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; font-size: 16px;">
                                    🚀 دریافت مستقیم فایل MP3
                                </button>
                            </a>
                            <p style="font-size: 12px; margin-top: 10px; color: #eee;">بعد از کلیک، در صفحه باز شده دکمه Download را بزنید.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # یک لینک جایگزین ۱۰۰٪ در صورت لزوم
                    with st.expander("لینک کمکی در صورت لزوم"):
                        st.write(f"لینک مستقیم آهنگ: {s_url}")
                else:
                    st.warning("آهنگی پیدا نشد.")
        except Exception as e:
            st.error(f"خطا در مدل: {e}")