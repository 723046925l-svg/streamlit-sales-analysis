import streamlit as st
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display

def arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    body {
        font-family: 'Cairo', Tahoma, Arial, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"<h1 style='direction: rtl; text-align: right;'>{arabic_text('لوحة تحكم مبيعات')}</h1>", unsafe_allow_html=True
)

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
    st.dataframe(df)  # البيانات الأصلية بدون reshaping

product_sales = df.groupby("المنتج")["الإجمالي"].sum().sort_values(ascending=False)
st.markdown(f"<h3 style='direction: rtl; text-align: right;'>{arabic_text('إجمالي المبيعات حسب المنتج')}</h3>", unsafe_allow_html=True)
st.bar_chart(product_sales)

branch_sales = df.groupby("الفرع")["الإجمالي"].sum().sort_values(ascending=False)
st.markdown(f"<h3 style='direction: rtl; text-align: right;'>{arabic_text('إجمالي المبيعات حسب الفرع')}</h3>", unsafe_allow_html=True)
st.bar_chart(branch_sales)

time_sales = df.groupby("تاريخ_الطلب")["الإجمالي"].sum()
st.markdown(f"<h3 style='direction: rtl; text-align: right;'>{arabic_text('تطور المبيعات عبر الزمن')}</h3>", unsafe_allow_html=True)
st.line_chart(time_sales)

best_product = product_sales.idxmax()
best_branch = branch_sales.idxmax()

st.markdown(f"<h3 style='direction: rtl; text-align: right;'>{arabic_text('توصيات')}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='direction: rtl; text-align: right;'>{arabic_text(f'أفضل منتج مبيعًا: {best_product}')}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='direction: rtl; text-align: right;'>{arabic_text(f'أفضل فرع من حيث المبيعات: {best_branch}')}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='direction: rtl; text-align: right;'>{arabic_text('ننصح بالتركيز التسويقي على المنتج والفرع الأفضل لتعزيز الأرباح.')}</p>", unsafe_allow_html=True)
