import streamlit as st
import pandas as pd
import joblib
from prophet.plot import plot_plotly
import plotly.graph_objs as go

# 1. Page Configuration
st.set_page_config(page_title="PharmaPredict AI", layout="wide", page_icon="💊")

# Custom CSS to make it look cleaner
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=100)
st.sidebar.title("Control Panel")
st.sidebar.markdown("---")

st.sidebar.subheader("🚚 Supply Chain Settings")
lead_time = st.sidebar.number_input("Lead Time (Days to receive stock)", min_value=1, max_value=30, value=3)
service_level = st.sidebar.select_slider(
    "Service Level (Confidence)",
    options=[0.90, 0.95, 0.99],
    value=0.95,
    help="Higher service level means more safety stock to prevent shortages."
)

# 3. Load Data & Model
@st.cache_resource
def load_assets():
    model = joblib.load('prophet_model_n02be.pkl')
    df = pd.read_csv('data/daily_sales_cleaned.csv')
    df['datum'] = pd.to_datetime(df['datum'])
    return model, df

try:
    model, df = load_assets()

    # --- MAIN CONTENT ---
    st.title("💊 PharmaPredict: AI Inventory Optimizer")
    st.info("Target Medicine: **N02BE (Analgesics & Antipyretics)**")

    # Create Tabs for better Organization
    tab1, tab2 = st.tabs(["📈 Demand Forecast", "📦 Inventory Strategy"])

    with tab1:
        st.subheader("AI-Driven Sales Prediction")
        st.write("This chart shows historical sales data and the AI's prediction for the next 30 days.")
        
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        
        fig = plot_plotly(model, forecast)
        fig.update_layout(title="Sales Trend & Forecast", xaxis_title="Date", yaxis_title="Units Sold")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Automated Inventory Planning")
        
        # Calculation Logic
        avg_demand = forecast.iloc[-30:]['yhat'].mean()
        std_error = 5.0 # This could be calculated dynamically from model residuals
        z_scores = {0.90: 1.28, 0.95: 1.645, 0.99: 2.33}
        
        safety_stock = z_scores[service_level] * std_error
        rop = (avg_demand * lead_time) + safety_stock
        
        # Display Metrics in Columns
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Avg. Predicted Demand", f"{avg_demand:.2f} units/day")
        with m2:
            st.metric("Required Safety Stock", f"{safety_stock:.2f} units")
        with m3:
            st.metric("Re-order Point (ROP)", f"{rop:.2f} units", delta_color="inverse")

        st.markdown("---")
        
        # Actionable Advice
        st.subheader("💡 Operational Guidance")
        if rop > 50: # Example logic
            st.warning(f"**Action Required:** Current calculated ROP is high. Ensure warehouse capacity for at least {rop:.0f} units.")
        
        st.success(f"""
        **How to use this:** 1. When your physical stock levels drop below **{rop:.2f} units**, place a new order.
        2. With a Lead Time of **{lead_time} days**, your new stock will arrive just before you run out.
        3. This setup guarantees a **{service_level*100:.0f}%** probability that you will not face a stockout.
        """)

        st.markdown("---")
        st.subheader("🛒 Procurement Action")
        
        # สร้างคอลัมน์สำหรับฟอร์มสั่งซื้อ
        col_order, col_status = st.columns([2, 1])
        
        with col_order:
            order_qty = st.number_input("Enter Order Quantity (Units)", min_value=1, value=int(rop))
            staff_id = st.text_input("Staff ID / Authorized Person", placeholder="e.g. PHARMA-101")
            
            # ปุ่มสั่งของ
            if st.button("🚀 Place Order Now", use_container_width=True):
                if staff_id:
                    # จำลองการทำงาน (Simulation)
                    st.balloons() # เอฟเฟกต์ฉลอง
                    st.session_state['order_sent'] = True
                    st.session_state['last_order'] = {"qty": order_qty, "id": staff_id}
                else:
                    st.error("Please enter Staff ID to authorize this order.")

        with col_status:
            st.write("**Order Status**")
            if 'order_sent' in st.session_state:
                st.success("✅ Order Sent!")
                st.write(f"**Qty:** {st.session_state['last_order']['qty']} units")
                st.write(f"**By:** {st.session_state['last_order']['id']}")
                st.caption("Sent to: procurement@hospital.com")
            else:
                st.info("No active orders.")

except Exception as e:
    st.error(f"Error loading application: {e}")