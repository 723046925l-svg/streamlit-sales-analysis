import streamlit as st
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display

def arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# ضبط اتجاه الصفحة ونوع الخط للكتابة بالعربي
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(arabic_text("لوحة تحكم مبيعات"))

@st.cache_data
def load_data():
    df = pd.read_excel("sales_data.xlsx")
    df["تاريخ_الطلب"] = pd.to_datetime(df["تاريخ_الطلب"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(arabic_text("خطأ: لم يتم العثور على ملف البيانات sales_data.xlsx"))
    st.stop()

if st.checkbox(arabic_text("عرض البيانات الخام")):
    st.dataframe(df)

# تجميع المبيعات حسب المنتج
product_sales = df.groupby("المنتج")["الإجمالي"].sum().sort_values(ascending=False)
st.subheader(arabic_text("إجمالي المبيعات حسب المنتج"))
st.bar_chart(product_sales)

# تجميع المبيعات حسب الفرع
branch_sales = df.groupby("الفرع")["الإجمالي"].sum().sort_values(ascending=False)
st.subheader(arabic_text("إجمالي المبيعات حسب الفرع"))
st.bar_chart(branch_sales)

# تطور المبيعات عبر الزمن
time_sales = df.groupby("تاريخ_الطلب")["الإجمالي"].sum()
st.subheader(arabic_text("تطور المبيعات عبر الزمن"))
st.line_chart(time_sales)

# أفضل منتج وأفضل فرع
best_product = product_sales.idxmax()
best_branch = branch_sales.idxmax()

st.subheader(arabic_text("توصيات"))
st.write(arabic_text(f"أفضل منتج مبيعًا: {best_product}"))
st.write(arabic_text(f"أفضل فرع من حيث المبيعات: {best_branch}"))
st.write(arabic_text("ننصح بالتركيز التسويقي على المنتج والفرع الأفضل لتعزيز الأرباح."))
