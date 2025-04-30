# streamlit_app.py
import streamlit as st
import main
import plotly.express as px
import pandas as pd
from datetime import datetime

st.title("Temperature Insights")

if "scraping" not in st.session_state:
    st.session_state.scraping = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "stop_time" not in st.session_state:
    st.session_state.stop_time = None

col1, col2 = st.columns(2)
if col1.button("Start"):
    st.session_state.scraping = True
    st.session_state.start_time = datetime.now()
    main.start_scraping()

if col2.button("Stop"):
    st.session_state.scraping = False
    st.session_state.stop_time = datetime.now()
    main.stop_scraping_func()

# Load and filter data
try:
    df = pd.read_csv("data.txt", names=["date", "temperature"])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d-%H-%M-%S", errors='coerce')
    df["temperature"] = pd.to_numeric(df["temperature"], errors='coerce')
    df.dropna(inplace=True)

    if st.session_state.start_time and st.session_state.stop_time:
        mask = (df["date"] >= st.session_state.start_time) & (df["date"] <= st.session_state.stop_time)
        df = df[mask]
        if not df.empty:
            fig = px.line(df, x="date", y="temperature", labels={"date": "Date", "temperature": "Temperature (°C)"})
            st.plotly_chart(fig)
        else:
            st.info("No available data in time frame please click start button")
except Exception as e:
    st.warning(f"No data available: {e}")