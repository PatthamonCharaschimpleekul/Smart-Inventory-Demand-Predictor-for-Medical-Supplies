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