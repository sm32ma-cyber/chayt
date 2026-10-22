import os
import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة وتصميمها
st.set_page_config(page_title="Maher Chat AI", page_icon="🤖", layout="centered")
st.title("🤖 Maher Chat AI")
st.caption("مساعدك الذكي المدعوم بـ Google Gemini")

# 2. جلب مفتاح الـ API بشكل آمن من الـ Secrets أو البيئة
# سيبحث الكود أولاً في أسرار Streamlit، ثم في متغيرات البيئة الافتراضية
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["AQ.Ab8RN6K1IATuvFdlYere1KvBXTgBq-fuhGmLR7_0tp44rubrvg"]
else:
    api_key = os.environ.get("AQ.Ab8RN6K1IATuvFdlYere1KvBXTgBq-fuhGmLR7_0tp44rubrvg")

# التحقق من وجود المفتاح
if not api_key:
    st.error("❌ لم يتم العثور على مفتاح GOOGLE_API_KEY. يرجى إضافته في إعدادات Advanced Settings -> Secrets")
    st.stop()

# 3. إعداد مكتبة Google Generative AI
genai.configure(api_key=api_key)

# 4. إعداد الذاكرة لحفظ محادثات المستخدم (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض الرسائل السابقة في الواجهة عند إعادة تحميل الصفحة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. صندوق إدخال النص للمستخدم
if user_input := st.chat_input("اكتب رسالتك هنا..."):
    
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # إنشاء تأثير الانتظار أثناء جلب الرد من Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # استدعاء النموذج (استخدام gemini-1.5-flash كخيار افتراضي سريع ومجاني)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            # إرسال الرسالة وجلب الرد
            response = model.generate_content(user_input)
            full_response = response.text
            
            # عرض الرد في الواجهة
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"⚠️ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
            message_placeholder.error(full_response)
            
    # حفظ رد البوت في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": full_response})
