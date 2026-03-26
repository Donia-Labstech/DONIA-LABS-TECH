import streamlit as st
from groq import Groq
from fpdf import FPDF
import datetime
import base64
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# 1. إعدادات الصفحة وإخفاء معالم Streamlit الافتراضية
st.set_page_config(page_title="DONIA MIND 1 - Exam Pro", page_icon="📝", layout="wide")

hide_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        text-align: right;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تحسين شكل منطقة النص */
    .stTextArea textarea {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. الربط مع Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ يرجى إضافة GROQ_API_KEY في إعدادات Secrets")

# 3. دالة تصدير PDF تدعم العربية (تحسين الجودة)
def export_pdf(text, subject_name):
    pdf = FPDF()
    pdf.add_page()
    
    # ملاحظة: يجب توفير ملف خط Cairo-Regular.ttf في مجلد المشروع
    try:
        pdf.add_font('Cairo', '', 'Cairo-Regular.ttf', uni=True)
        pdf.set_font('Cairo', '', 16)
    except:
        pdf.set_font("Arial", size=12) # خط بديل في حال عدم وجود الملف
    
    # معالجة النص العربي ليظهر بشكل صحيح
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    
    pdf.cell(200, 10, txt=get_display(reshape("منظومة DONIA MIND 1 التعليمية")), ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=bidi_text, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 4. واجهة التطبيق
st.title("🛡️ منظومة DONIA MIND الاحترافية")
st.subheader("الجيل الثالث - دعم الذكاء الاصطناعي البصري")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ تخصيص الوكيل")
    subject = st.selectbox("اختر مادة الاختبار:", 
        ["الرياضيات", "فيزياء", "علوم الطبيعة", "اللغة العربية", "الإسبانية", "الألمانية", "التاريخ والجغرافيا"])
    
    mode = st.radio("نوع العمل:", [
        "إنشاء نموذج اختبار", 
        "تحليل وتنقيط إجابة",
        "تحليل صورة (Vision Mode) 👁️"
    ])
    
    st.divider()
    if mode == "تحليل صورة (Vision Mode) 👁️":
        uploaded_file = st.file_uploader("ارفع صورة الاختبار أو إجابة الطالب:", type=['png', 'jpg', 'jpeg'])
    
    st.caption("النسخة v3.0 - دعم LaTeX & Vision")

# 5. منطقة العمل
user_input = st.text_area("أدخل نص السؤال، أو تفاصيل إضافية للصورة:", height=150)

if st.button("🚀 تنفيذ المهمة"):
    if user_input or (mode == "تحليل صورة (Vision Mode) 👁️" and uploaded_file):
        try:
            with st.spinner('جاري المعالجة بواسطة الذكاء الاصطناعي...'):
                
                # --- حالة تحليل الصور (Vision Model) ---
                if mode == "تحليل صورة (Vision Mode) 👁️" and uploaded_file:
                    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                    completion = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview", # موديل الرؤية
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"قم بتحليل هذه الصورة لمادة {subject}. إذا كان اختباراً قم بحله، وإذا كانت إجابة طالب قم بتصحيحها بدقة باستخدام LaTeX."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ],
                        temperature=0.5,
                    )
                
                # --- حالة النصوص العادية ---
                else:
                    if mode == "إنشاء نموذج اختبار":
                        instruction = f"أنت وكيل {subject} خبير. قم بإنشاء نموذج اختبار احترافي يتضمن أسئلة متنوعة. استخدم LaTeX للمعادلات. ضع سلم تنقيط."
                    else:
                        instruction = f"أنت مصحح خبير في {subject}. قم بتحليل الإجابة التالية، قدم تنقيطاً من 20، ووضح الأخطاء بدقة."

                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": instruction},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                    )

                result = completion.choices[0].message.content
                
                # عرض النتائج
                st.markdown("### 🤖 النتيجة الاحترافية:")
                st.info(f"المادة: {subject} | الوضع: {mode}")
                st.markdown(result)

                # خيار التحميل
                pdf_data = export_pdf(result, subject)
                st.download_button(
                    label="📥 تحميل الوثيقة كـ PDF (نسخة محسنة)",
                    data=pdf_data,
                    file_name=f"Donia_Mind_{subject}_{datetime.date.today()}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
    else:
        st.warning("الرجاء إدخال نص أو رفع صورة للبدء.")
