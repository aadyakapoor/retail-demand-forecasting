import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "https://retail-demand-forecasting-sua5.onrender.com"

st.set_page_config(page_title="Demand Forecasting Dashboard", layout="wide")

st.title("📦 Retail Demand Forecasting Dashboard")
st.markdown(
    "Forecasts daily unit sales using a LightGBM model trained on Walmart M5 data."
)

st.sidebar.header("Forecast Settings")


@st.cache_data(ttl=300)
def get_items():
    try:
        response = requests.get(f"{API_URL}/items", timeout=60)
        return response.json()["items"]
    except Exception as e:
        st.error(f"Could not connect to API: {e}")
        return []


items = get_items()

if not items:
    st.warning(
        "Waking up the API — this can take 30-50 seconds on first load."
    )
    st.stop()

item_id = st.sidebar.selectbox("Select Item", items)

horizon = st.sidebar.slider(
    "Forecast Horizon (days)",
    min_value=7,
    max_value=60,
    value=28
)

if st.sidebar.button("Generate Forecast", type="primary"):

    with st.spinner("Generating forecast..."):

        response = requests.post(
            f"{API_URL}/forecast",
            json={
                "item_id": item_id,
                "horizon": horizon
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        forecast_df = pd.DataFrame(data["forecast"])
        forecast_df["date"] = pd.to_datetime(
            forecast_df["date"]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Item",
            item_id.split("_evaluation")[0]
        )

        col2.metric(
            "Avg Predicted Daily Sales",
            f"{forecast_df['predicted_sales'].mean():.1f}"
        )

        col3.metric(
            "Forecast Horizon",
            f"{horizon} days"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=forecast_df["date"],
                y=forecast_df["predicted_sales"],
                mode="lines+markers",
                name="Predicted Sales"
            )
        )

        fig.update_layout(
            title=f"Demand Forecast — {item_id}",
            xaxis_title="Date",
            yaxis_title="Predicted Sales",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            forecast_df,
            use_container_width=True
        )

else:
    st.info(
        "Select an item and click Generate Forecast."
    )