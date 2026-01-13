import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Netflix Subscription Forecast",
    page_icon="📈",
    layout="wide"
)

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    return joblib.load("arima_netflix_model.pkl")

model = load_model()

# -------------------------------
# Title & Description
# -------------------------------
st.title("📊 Netflix Subscription Forecasting")
st.markdown("""
This application forecasts **Netflix subscription growth** using a  
**Time Series ARIMA model** trained on historical quarterly data.
""")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("Forecast Settings")

forecast_steps = st.sidebar.slider(
    "Select number of quarters to forecast",
    min_value=4,
    max_value=15,
    value=8
)

# -------------------------------
# Generate Forecast
# -------------------------------
forecast = model.forecast(steps=forecast_steps)

forecast_df = pd.DataFrame({
    "Quarter": range(1, forecast_steps + 1),
    "Forecasted Subscribers (Millions)": forecast.values
})

# -------------------------------
# Display Forecast Table
# -------------------------------
st.subheader("📋 Forecasted Subscription Values")
st.dataframe(forecast_df, use_container_width=True)

# -------------------------------
# Plot Forecast
# -------------------------------
st.subheader("📈 Forecast Visualization")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=forecast_df["Quarter"],
    y=forecast_df["Forecasted Subscribers (Millions)"],
    mode="lines+markers",
    name="Forecast"
))

fig.update_layout(
    title="Netflix Subscription Forecast",
    xaxis_title="Quarters Ahead",
    yaxis_title="Subscribers (Millions)",
    template="plotly_white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Model Explanation Section
# -------------------------------
with st.expander("ℹ️ Model Explanation"):
    st.markdown("""
    **ARIMA (AutoRegressive Integrated Moving Average)** is a classical time series
    forecasting technique that models trends and temporal dependencies.

    **Why ARIMA?**
    - Subscription data is time-dependent
    - Captures trend and momentum
    - Effective for short- to medium-term forecasting

    **Limitations**
    - Assumes linear patterns
    - Less effective with strong seasonality or sudden shocks
    """)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("🚀 *Built for ML Portfolio & Deployment Demonstration*")
