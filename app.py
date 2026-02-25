import streamlit as st
import openpyxl
from io import BytesIO

st.set_page_config(page_title="مصلح الأرقام - النسخة النهائية", layout="centered")

st.title("🇪🇬 مصلح أرقام الموبايل (حل مشكلة التنسيق)")
st.write("النسخة دي بتجبر الإكسيل إنه يظهر الرقم صح من غير ما يعتبره معادلة.")

uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا", type=["xlsx"])

if uploaded_file:
    wb = openpyxl.load_workbook(uploaded_file)
    sheet = wb.active
    
    cols = [cell.column_letter for cell in sheet[1]]
    col_letter = st.selectbox("اختار حرف العمود:", cols)

    if st.button("تعديل وحفظ الملف"):
        def clean_and_fix(val):
            if val is None: return None
            
            s = str(val).strip()
            if s.endswith('.0'): s = s[:-2]
            s = s.replace('+', '').replace("'", "") # تنظيف أي علامات قديمة
            
            if s == "": return None

            # منطق التصليح اللي اتفقنا عليه
            if s.startswith("2001"):
                s = "201" + s[4:]
            elif s.startswith("1") and not s.startswith("20"):
                s = "20" + s
            elif s.startswith("01"):
                s = "20" + s[1:]
            elif not s.startswith("20"):
                s = "20" + s

            # الحل السحري: إضافة ' قبل الـ +
            # دي بتخلي الإكسيل يفهم إن ده نص (Text) مش عملية حسابية
            return f"'+{s}"

        for row in range(1, sheet.max_row + 1):
            cell = sheet[f"{col_letter}{row}"]
            fixed_value = clean_and_fix(cell.value)
            
            if fixed_value:
                cell.value = fixed_value
                # تأكيد إضافي إن نوع الخلية نص
                cell.data_type = 's'

        output = BytesIO()
        wb.save(output)
        
        st.success("✅ تم الإصلاح! جرب نزل الملف دلوقتي وهتلاقيه اتظبط.")
        st.download_button(
            label="تحميل الملف المعدل 📥",
            data=output.getvalue(),
            file_name="Fixed_Mobile_Numbers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
