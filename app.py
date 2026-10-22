import os
import streamlit as st
import google.generativeai as genai

# إعداد الصفحة والواجهة
st.set_page_config(page_title="Maher Chat AI", page_icon="🤖", layout="centered")
st.title("🤖 Maher Chat AI")
st.caption("مساعدك الذكي المدعوم بـ Google Gemini")

# جلب المفتاح بأمان من الأسرار دون كتابته هنا علناً
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = os.environ.get("GOOGLE_API_KEY")

# التحقق من وجود المفتاح لمنع توقف التطبيق
if not api_key:
    st.error("❌ لم يتم العثور على مفتاح GOOGLE_API_KEY. يرجى إضافته في إعدادات Secrets")
    st.stop()

# إعداد مكتبة الذكاء الاصطناعي
genai.configure(api_key=api_key)

# إعداد الذاكرة لحفظ الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق إدخال النص واستقبال الإجابة
if user_input := st.chat_input("اكتب رسالتك هنا..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # استدعاء نموذج جيميناي
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
            message_placeholder.error(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
