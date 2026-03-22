import streamlit as st
import pandas as pd
import joblib
from prophet.plot import plot_plotly
import plotly.graph_objs as go

# 1. Page Configuration
st.set_page_config(page_title="PharmaPredict AI", layout="wide", page_icon="💊")

# Custom CSS for a clean, professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar: Navigation & Settings
st.sidebar.title("🎮 Control Panel")
st.sidebar.markdown("---")

# Drug Selection
st.sidebar.subheader("🎯 Select Medicine")
drug_list = ['N02BE', 'N05B', 'R03']
selected_drug = st.sidebar.selectbox("Target Drug Code", drug_list)

# Project Note
st.sidebar.info("""
**Note:** This is a prototype for demonstration. 
We have selected the **Top 3 high-volume drugs** to showcase AI forecasting and inventory logic.
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🚚 Supply Chain Settings")
lead_time = st.sidebar.number_input("Lead Time (Days to receive stock)", 1, 30, 3)
service_level = st.sidebar.select_slider(
    "Service Level (Confidence)",
    options=[0.90, 0.95, 0.99],
    value=0.95,
    help="Higher service level increases safety stock to prevent shortages."
)

# 3. Data & Model Loading
@st.cache_resource
def load_assets(drug_name):
    # Dynamic path based on selected drug
    model_path = f'prophet_model_{drug_name.lower()}.pkl'
    model = joblib.load(model_path)
    # Ensure this path matches your GitHub structure
    df = pd.read_csv('data/daily_sales_cleaned.csv') 
    df['datum'] = pd.to_datetime(df['datum'])
    return model, df

try:
    model, df = load_assets(selected_drug)

    # --- MAIN INTERFACE ---
    st.title("🏥 Smart Pharma Inventory Dashboard")
    st.markdown(f"Currently Analyzing: **{selected_drug}**")

    tab1, tab2 = st.tabs(["📈 Demand Forecast", "📦 Inventory Strategy"])

    with tab1:
        st.subheader("AI-Driven Sales Prediction")
        
        # 30-Day Forecast
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        # Custom Plotly Graph with Legend
        fig = go.Figure()
        
        # Actual Data
        fig.add_trace(go.Scatter(x=df['datum'], y=df[selected_drug], 
                                 name='Actual Sales', mode='markers', 
                                 marker=dict(color='black', size=4)))
        
        # AI Forecast
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], 
                                 name='AI Forecast', mode='lines', 
                                 line=dict(color='#007bff', width=2)))
        
        # Confidence Interval
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], 
                                 mode='lines', line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], 
                                 mode='lines', line=dict(width=0), 
                                 fill='tonexty', fillcolor='rgba(0, 123, 255, 0.2)', 
                                 name='Uncertainty Interval'))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Units Sold",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Inventory Optimization (ROP Model)")
        
        # Inventory Logic
        avg_demand = forecast.iloc[-30:]['yhat'].mean()
        # std_error can be calculated from model residuals; here we use 5.0 as a safe constant for the demo
        std_error = 5.0 
        z_scores = {0.90: 1.28, 0.95: 1.645, 0.99: 2.33}
        
        safety_stock = z_scores[service_level] * std_error
        rop = (avg_demand * lead_time) + safety_stock
        
        # Key Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Avg. Demand", f"{avg_demand:.2f} units/day")
        m2.metric("Safety Stock Required", f"{safety_stock:.2f} units")
        m3.metric("Re-order Point (ROP)", f"{rop:.2f} units")

        st.markdown("---")
        
        # Order Simulation
        st.subheader("🛒 Procurement Simulation")
        col_form, col_status = st.columns([2, 1])
        
        with col_form:
            order_qty = st.number_input("Order Quantity", min_value=1, value=int(rop))
            staff_id = st.text_input("Authorizing Staff ID", placeholder="e.g., PHARMA-99")
            
            if st.button("Place Supply Order", use_container_width=True):
                if staff_id:
                    st.balloons()
                    st.session_state['order_sent'] = True
                    st.session_state['last_order'] = {"qty": order_qty, "id": staff_id, "drug": selected_drug}
                else:
                    st.error("Identification required to process order.")

        with col_status:
            st.write("**Transaction Status**")
            if 'order_sent' in st.session_state:
                st.success(f"Order Successful!")
                st.write(f"**Drug:** {st.session_state['last_order']['drug']}")
                st.write(f"**Qty:** {st.session_state['last_order']['qty']}")
                st.write(f"**Authorized By:** {st.session_state['last_order']['id']}")
            else:
                st.info("Awaiting user action.")

except Exception as e:
    st.error(f"System Error: Unable to initialize dashboard. Please ensure all model files are uploaded. Details: {e}")