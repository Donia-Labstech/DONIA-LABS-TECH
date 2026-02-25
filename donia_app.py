import streamlit as st
import ollama

st.set_page_config(page_title="DONIA MIND1 - Agent System", layout="wide")

st.title("🧠 منظومة DONIA MIND1 للوكلاء الأذكياء")
st.sidebar.header("إدارة الوكلاء")

# اختيار الوكيل المختص
agent_type = st.sidebar.selectbox(
    "اختر المعلم الذكي:",
    ["وكيل إدارة المهام", "معلم العلوم الطبيعية", "معلم الرياضيات", "معلم الفيزياء"]
)

st.write(f"📡 أنت الآن تتصل بـ: **{agent_type}** عبر سحابة Minimax")

# مساحة الدردشة مع الوكيل
user_input = st.text_input(f"ماذا تطلب من {agent_type}؟")

if st.button("إرسال الطلب"):
    with st.spinner("جاري معالجة الطلب عبر الوكيل الفرعي..."):
        # هنا يتم توجيه الطلب للسحابة بناءً على تخصص الوكيل
        response = ollama.generate(
            model='minimax-m2.5:cloud',
            prompt=f"أنت {agent_type}. بصفتك خبيراً في المنهج الجزائري، أجب على: {user_input}"
        )
        st.chat_message("assistant").write(response['response'])