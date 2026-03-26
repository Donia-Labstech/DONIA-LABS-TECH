import ollama
import subprocess
import os
from jinja2 import Template

class DoniaMind:
    import ollama
import subprocess
from jinja2 import Template
import os

class DoniaMindCloud:
    def __init__(self):
        self.client = ollama.Client(host='http://localhost:11434')
        # سنستخدم الموديل السحابي الذي يدعم البحث والوكلاء
        self.model = 'minimax-m2.5:cloud' 

    def generate_smart_exam(self, topic, level):
        print(f"🌐 DONIA MIND1 يتصل بالسحابة لتحليل: {topic}...")
        
        # البرومبت المطور للاستفادة من قدرات البحث
        prompt = f"""
        قم بالبحث عن أحدث المواضيع المتعلقة بـ {topic} للمستوى {level}.
        أنشئ اختباراً احترافياً بصيغة LaTeX مستخدماً بيئة 'enumerate'.
        ركز على الأسئلة التي تقيس الفهم العميق. باللغة العربية.
        أعطني كود الأسئلة فقط.
        """
        
        try:
            # هنا نستخدم خاصية البحث إذا كانت مفعلة في نسخة Ollama لديك
            response = self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"عذراً، تأكد من سحب الموديل السحابي أولاً. الخطأ: {str(e)}"

    def build_pdf(self, subject, level):
        content = self.generate_smart_exam(subject, level)
        
        with open('template.tex', 'r', encoding='utf-8') as f:
            tmpl = Template(f.read())
        
        final_tex = tmpl.render(SUBJECT=subject, LEVEL=level, CONTENT=content)
        
        with open('donia_cloud_exam.tex', 'w', encoding='utf-8') as f:
            f.write(final_tex)
        
        print("📑 جاري معالجة الملف السحابي عبر LaTeX...")
        subprocess.run(['pdflatex', 'donia_cloud_exam.tex'], stdout=subprocess.DEVNULL)
        print(f"✨ نجاح! تم استخراج الامتحان السحابي: donia_cloud_exam.pdf")

if __name__ == "__main__":
    mind = DoniaMindCloud()
    s = input("المادة المطلوبة: ")
    l = input("المستوى (مثلاً BEM): ")
    mind.build_pdf(s, l)
