import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="مصلح أرقام الموبايل المصرية", layout="centered")

st.title("🇪🇬 أداة تنسيق وتنظيف أرقام الموبايل")
st.write("ارفع ملف الإكسيل وهيظبطلك الأرقام (يزود +20، يشيل الأصفار الزيادة، ويصلح النواقص)")

# رفع الملف
uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا (xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    column_name = st.selectbox("اختار العمود اللي فيه الأرقام:", df.columns)
    
    if st.button("ابدأ المعالجة"):
        def fix_egyptian_number(val):
            # 1. التأكد إن الخلية مش فاضية
            if pd.isna(val) or str(val).strip() == "":
                return ""
            
            # 2. تحويل النص لنص وتنظيف المسافات وعلامة الزائد القديمة لو موجودة
            num = str(val).strip().replace("+", "")
            
            # 3. معالجة حالة الصفر الزيادة (مثال: 20010 -> 2010)
            if num.startswith("2001"):
                num = "201" + num[4:]
            
            # 4. معالجة حالة الرقم اللي بيبدأ بـ 1 علطول (مثال: 100 -> 20100)
            elif num.startswith("1") and not num.startswith("201"):
                num = "20" + num
            
            # 5. معالجة حالة الرقم اللي بيبدأ بـ 01 (مثال: 010 -> 2010)
            elif num.startswith("01"):
                num = "20" + num[1:]
            
            # 6. لو الرقم مش بيبدأ بـ 20 خالص وهو رقم موبايل (مثلاً بدأ بـ 11 أو 12)
            elif (num.startswith("10") or num.startswith("11") or num.startswith("12") or num.startswith("15")) and not num.startswith("20"):
                 num = "20" + num

            # إرجاع الرقم بالتنسيق النهائي
            return f"+{num}"

        # تطبيق الدالة على العمود المختار
        df[column_name] = df[column_name].astype(str).apply(fix_egyptian_number)
        
        # تحويل النتيجة لملف إكسيل
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        processed_data = output.getvalue()
        
        st.success("✅ تم تنظيف وتنسيق الأرقام بنجاح!")
        st.download_button(
            label="تحميل الملف المعدل 📥",
            data=processed_data,
            file_name="Formatted_Egyptian_Numbers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.info("ملاحظة: الكود بيتعامل مع الأرقام كـ Text عشان يحافظ على علامة الـ (+) والأصفار.")
