import streamlit as st
import pandas as pd
import plotly.express as px

st.title("VR Object Movement Tracking")

uploaded_file = st.file_uploader("Upload a CSV log file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview", df.head())

    # Example: Player trajectory (X vs Z over time)
    fig = px.line(
        df,
        x="Time",
        y=["PlayerX", "PlayerZ"],  # plot multiple columns
        title="Player Movement Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Example: Dynamic objects positions
    for col in [c for c in df.columns if "Elephant" in c or "Truck" in c]:
        fig2 = px.line(df, x="Time", y=col, title=f"{col} Position")
        st.plotly_chart(fig2, use_container_width=True)
