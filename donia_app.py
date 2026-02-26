import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime

# 1. إعداد واجهة المستخدم
st.set_page_config(page_title="DONIA MIND 1 - Exam Pro", page_icon="📝", layout="wide")

# 2. الربط مع محرك Groq المجاني (ضع مفتاحك في Secrets باسم GROQ_API_KEY)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ يرجى إضافة GROQ_API_KEY في إعدادات Secrets")

# 3. دالة إنشاء ملف PDF احترافي
def export_pdf(content, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="DONIA MIND 1 - Academic System", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# 4. واجهة التطبيق
st.title("🛡️ منظومة DONIA MIND الاحترافية للاختبارات")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ تخصيص الوكيل")
    subject = st.selectbox("اختر مادة الاختبار:", 
        ["الرياضيات", "فيزياء", "علوم الطبيعة", "اللغة العربية", "الإسبانية", "الألمانية"])
    mode = st.radio("نوع العمل:", ["إنشاء نموذج اختبار", "تحليل وتنقيط إجابة"])
    st.divider()
    st.caption("النسخة v3.0 - دعم LaTeX & PDF")

# 5. منطقة العمل
user_input = st.text_area("أدخل نص السؤال أو إجابة الطالب للتحليل:", height=200)

if st.button("🚀 تنفيذ المهمة"):
    if user_input:
        try:
            with st.spinner('جاري المعالجة بواسطة الذكاء الاصطناعي...'):
                # بناء الـ Prompt الاحترافي
                if mode == "إنشاء نموذج اختبار":
                    instruction = f"أنت وكيل {subject}. قم بإنشاء نموذج اختبار احترافي يتضمن أسئلة اختيار من متعدد وأسئلة مقالية. استخدم LaTeX للمعادلات. ضع سلم تنقيط مقترح."
                else:
                    instruction = f"أنت مصحح خبير في {subject}. قم بتحليل إجابة الطالب التالية، قدم تنقيطاً دقيقاً من 20، ووضح الأخطاء مع التصحيح النموذجي باستخدام LaTeX."

                completion = client.chat.completions.create(
                    model="model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                )

                result = completion.choices[0].message.content
                
                # عرض النتائج
                st.markdown("### 🤖 النتيجة الاحترافية:")
                st.markdown(result) # هنا سيظهر الـ LaTeX بشكل تلقائي إذا استخدم الوكيل $ $

                # خيار التحميل
                pdf_data = export_pdf(result, subject)
                st.download_button(
                    label="📥 تحميل الوثيقة كـ PDF",
                    data=pdf_data,
                    file_name=f"Donia_Mind_{subject}_{datetime.date.today()}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("الرجاء إدخال البيانات أولاً.")