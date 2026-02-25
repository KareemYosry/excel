import streamlit as st
import openpyxl
from io import BytesIO

st.set_page_config(page_title="معالج ملفات الإكسيل", layout="wide")

st.title("🚀 معالجة ملفات الإكسيل ")

# رفع ملفات متعددة
uploaded_files = st.file_uploader("ارفع ملفات الإكسيل هنا", type=["xlsx"], accept_multiple_files=True)

# خانة تحديد العمود (افتراضي B)
col_letter = st.text_input("اكتب حرف العمود اللي فيه الأرقام (مثلاً A أو B):", "B").upper()

if uploaded_files:
    st.divider()
    st.subheader("الملفات الجاهزة للتحميل:")
    
    # عمل صفوف (Columns) في الويبسايت عشان الشكل يبقى منظم
    for uploaded_file in uploaded_files:
        # 1. فتح الملف ومعالجته في الذاكرة
        wb = openpyxl.load_workbook(uploaded_file)
        sheet = wb.active
        
        def clean_final(val):
            if val is None: return None
            s = str(val).strip()
            if s.endswith('.0'): s = s[:-2]
            s = s.replace('+', '').replace("'", "").replace('=', '')
            if s == "" or not s.isdigit(): return s
            
            # منطق التصليح المصري
            if s.startswith("2001"): s = "201" + s[4:]
            elif s.startswith("1") and not s.startswith("20"): s = "20" + s
            elif s.startswith("01"): s = "20" + s[1:]
            elif not s.startswith("20"): s = "20" + s
            return f"+{s}"

        # تطبيق التعديلات على العمود
        for row in range(1, sheet.max_row + 1):
            cell = sheet[f"{col_letter}{row}"]
            cell.number_format = '@' 
            cell.value = clean_final(cell.value)

        # 2. حفظ الملف المعدل في الذاكرة
        output = BytesIO()
        wb.save(output)
        processed_data = output.getvalue()

        # 3. عرض الملف في الواجهة مع زرار تحميل خاص به بنفس الاسم
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📄 {uploaded_file.name}")
        with col2:
            st.download_button(
                label="تحميل المعدل 📥",
                data=processed_data,
                file_name=uploaded_file.name, # هنا بنستخدم نفس الاسم الأصلي
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=uploaded_file.name # مفتاح فريد لكل زرار
            )
