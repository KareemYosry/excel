import streamlit as st
import openpyxl
from io import BytesIO

st.set_page_config(page_title="مصلح الأرقام - النسخة الاحترافية", layout="centered")

st.title("🇪🇬 مصلح الأرقام المصري (بدون أخطاء)")
st.write("النسخة دي بتغير تنسيق العمود لـ Text عشان الرقم يظهر صح 100%.")

uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا", type=["xlsx"])

if uploaded_file:
    wb = openpyxl.load_workbook(uploaded_file)
    sheet = wb.active
    
    cols = [cell.column_letter for cell in sheet[1]]
    col_letter = st.selectbox("اختار حرف العمود:", cols)

    if st.button("تعديل وحفظ الملف"):
        def clean_final(val):
            if val is None: return None
            
            s = str(val).strip()
            if s.endswith('.0'): s = s[:-2]
            
            # تنظيف شامل لأي عك قديم (علامات تنصيص أو يساوي)
            s = s.replace('+', '').replace("'", "").replace('=', '')
            
            if s == "" or not s.isdigit(): return s

            # منطق التصليح
            if s.startswith("2001"): s = "201" + s[4:]
            elif s.startswith("1") and not s.startswith("20"): s = "20" + s
            elif s.startswith("01"): s = "20" + s[1:]
            elif not s.startswith("20"): s = "20" + s

            return f"+{s}"

        # التنفيذ
        for row in range(1, sheet.max_row + 1):
            cell = sheet[f"{col_letter}{row}"]
            
            # 1. تحويل تنسيق الخلية لـ "Text" قبل وضع القيمة
            cell.number_format = '@' 
            
            # 2. الحصول على القيمة الجديدة
            new_val = clean_final(cell.value)
            
            # 3. وضع القيمة (بايثون هيبعتها كـ String صافي)
            cell.value = new_val

        output = BytesIO()
        wb.save(output)
        
        st.success("✅ تم الإصلاح! الرقم هيظهر +20 علطول وشكله نظيف.")
        st.download_button(
            label="تحميل الملف المعدل 📥",
            data=output.getvalue(),
            file_name="Clean_Egyptian_Numbers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
