import streamlit as st
import pandas as pd
import joblib
from prophet.plot import plot_plotly

#set up web page
st.set_page_config(page_title="Smart Phamar AI", layout="wide")

st.title("🏥 Smart Pharma Inventory Dashboard")
st.markdown("""
This application uses **Prophet AI** to predict drug demand and calculates the **Re-order Point (ROP)** using Management Engineering principles.
""")

#load model data
@st.cache_resource #use cache for quickly loading
def load_assets():
    model = joblib.load('prophet_model_n02be.pkl')
    df = pd.read_csv('data/daily_sales_cleaned.csv')
    df['datum'] = pd.to_datetime(df['datum'])
    return model, df

try:
    model, df = load_assets()

    st.sidebar.header("📦 Inventory Settings")
    lead_time = st.sidebar.slider("Lead Time (Days)", 1, 14, 3)
    service_level = st.sidebar.selectbox("Service Level", [0.90, 0.95, 0.99], index=1)

    col1, col2, = st.columns([3, 1])

    with col1:
        st.subheader("📈 30-Day Sales Forecast (N02BE)")
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        
        # กราฟ Interactive (ซูมได้ ขยับได้)
        fig = plot_plotly(model, forecast)
        st.plotly_chart(fig, use_container_config=True)

    with col2:
        st.subheader("🛡️ Inventory Metrics")
        # คำนวณ ROP แบบ Real-time ตามค่าที่ปรับใน Sidebar
        avg_demand = forecast.iloc[-30:]['yhat'].mean()
        # สมมติค่า std_error จากการเทรน (คุณสามารถคำนวณจริงจากไฟล์ train_model ได้)
        std_error = 5.0 
        z_dict = {0.90: 1.28, 0.95: 1.645, 0.99: 2.33}
        
        safety_stock = z_dict[service_level] * std_error
        rop = (avg_demand * lead_time) + safety_stock
        
        st.metric("Predicted Avg Demand", f"{avg_demand:.2f}")
        st.metric("Safety Stock", f"{safety_stock:.2f}")
        st.error(f"Re-order Point: {rop:.2f}")
        st.info("💡 Action: Order when stock < ROP")    

except FileNotFoundError:
    st.error("❌Model file or Data file not found. Pleaase run train_model.py first!")