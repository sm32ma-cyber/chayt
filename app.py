import os
import streamlit as st

# استدعاء المفتاح بشكل آمن من متغيرات البيئة
GOOGLE_API_KEY = os.environ.get("AQ.Ab8RN6K1IATuvFdlYere1KvBXTgBq-fuhGmLR7_0tp44rubrvg") 
# أو عبر نظام حماية Streamlit الخاص:
# GOOGLE_API_KEY = st.secrets["AQ.Ab8RN6K1IATuvFdlYere1KvBXTgBq-fuhGmLR7_0tp44rubrvg"]
