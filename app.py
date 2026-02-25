import streamlit as st
import openpyxl
from io import BytesIO

st.set_page_config(page_title="مصلح الأرقام (حافظ على التنسيق)", layout="centered")

st.title("🇪🇬 أداة تنسيق الأرقام مع الحفاظ على شكل الملف")
st.write("البرنامج ده هيعدل الأرقام ويسيب الألوان والمقاسات زي ما هي بالظبط.")

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا (xlsx)", type=["xlsx"])

if uploaded_file:
    # تحميل الملف الأصلي باستخدام openpyxl للحفاظ على التنسيق
    wb = openpyxl.load_workbook(uploaded_file)
    sheet = wb.active # بيختار أول Sheet

    # اختيار العمود (A, B, C...)
    # بنجيب أسماء العواميد من أول سطر عشان نسهل على المستخدم الاختيار
    cols = [cell.column_letter for cell in sheet[1]]
    col_letter = st.selectbox("اختار حرف العمود اللي فيه الأرقام (مثلاً A أو B):", cols)

    if st.button("تعديل وحفظ الملف"):
        def clean_and_fix(val):
            if val is None:
                return None
            
            # تحويل القيمة لنص وتنظيفها
            s = str(val).strip()
            
            # 1. إزالة الـ .0 اللي بتظهر مع الأرقام
            if s.endswith('.0'):
                s = s[:-2]
            
            # إزالة علامة + لو موجودة عشان نصلح الرقم براحتنا
            s = s.replace('+', '')
            
            if s == "":
                return None

            # 2. معالجة حالة الصفر الزيادة (20010 -> 2010)
            if s.startswith("2001"):
                s = "201" + s[4:]
            
            # 3. معالجة حالة الرقم اللي بيبدأ بـ 1 (زي 100 -> 20100)
            elif s.startswith("1") and not s.startswith("20"):
                s = "20" + s
                
            # 4. معالجة حالة الـ 01 (010 -> 2010)
            elif s.startswith("01"):
                s = "20" + s[1:]
            
            # 5. التأكد إن الرقم بيبدأ بـ 20
            if not s.startswith("20"):
                s = "20" + s

            return "+" + s

        # المرور على كل الصفوف في العمود المختار
        # بنبدأ من صف 1 (عشان ياخد أول سطر معاك زي ما طلبت)
        for row in range(1, sheet.max_row + 1):
            cell = sheet[f"{col_letter}{row}"]
            original_value = cell.value
            
            fixed_value = clean_and_fix(original_value)
            
            # وضع القيمة الجديدة في الخلية (التنسيق بيفضل زي ما هو تلقائياً)
            cell.value = fixed_value
            # التأكد إن الخلية متسجلة كـ Text عشان الإكسيل ميبوظش الـ +
            cell.data_type = 's' 

        # حفظ الملف في الذاكرة
        output = BytesIO()
        wb.save(output)
        processed_data = output.getvalue()

        st.success("✅ تم التعديل بنجاح مع الحفاظ على كل التنسيقات!")
        st.download_button(
            label="تحميل الملف المعدل 📥",
            data=processed_data,
            file_name="Formatted_Preserved_Style.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
