import streamlit as st
import main
import plotly.express as px
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Temperature Insights", layout="wide")
st.title("🌡️ Temperature Insights")

# Initialize session state
if "scraping" not in st.session_state:
    st.session_state.scraping = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "stop_time" not in st.session_state:
    st.session_state.stop_time = None

# Control buttons
col1, col2 = st.columns(2)

if col1.button("▶️ Start Scraping"):
    st.session_state.scraping = True
    st.session_state.start_time = datetime.now()
    st.session_state.stop_time = None
    main.start_scraping()

if col2.button("⏹️ Stop Scraping"):
    st.session_state.scraping = False
    st.session_state.stop_time = datetime.now()
    main.stop_scraping_func()

# Scraping status
if st.session_state.scraping:
    st.success(f"Scraping started at {st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    if st.session_state.stop_time:
        st.info(f"Scraping stopped at {st.session_state.stop_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.info("Scraping is not currently active.")

# Display temperature graph
try:
    df = main.read_content()
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d-%H-%M-%S", errors='coerce')
    df["temperature"] = pd.to_numeric(df["temperature"], errors='coerce')
    df.dropna(inplace=True)

    # Filter by start and stop time
    if st.session_state.start_time:
        end_time = st.session_state.stop_time or datetime.now()
        mask = (df["date"] >= st.session_state.start_time) & (df["date"] <= end_time)
        df_filtered = df[mask]

        if not df_filtered.empty:
            fig = px.line(df_filtered, x="date", y="temperature",
                          labels={"date": "Date", "temperature": "Temperature (°C)"},
                          title="📈 Temperature Over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available in the selected time frame.")
    else:
        st.info("Click 'Start Scraping' to begin collecting data.")

except Exception as e:
    st.error(f"An error occurred while loading data: {e}")