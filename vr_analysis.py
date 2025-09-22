import streamlit as st
import pandas as pd
import plotly.express as px

st.title("VR Object Replay (2D)")

uploaded_file = st.file_uploader("Upload VR log CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Flatten Unity (X,Z), ignore Y
    df["pos_x"] = df["pos_x"]
    df["pos_y"] = df["pos_z"]

    df["object"] = df["object"].astype(str)

    fig = px.scatter(
        df,
        x="pos_x",
        y="pos_y",
        color="object",
        animation_frame="time",
        animation_group="object",
        hover_name="object",
        title="2D Top-Down Replay (X–Z Plane)"
    )

    fig.update_layout(
        yaxis=dict(scaleanchor="x", scaleratio=1),
        width=800,
        height=800
    )

    st.plotly_chart(fig)
else:
    st.info("Please upload a `vr_log.csv` file.")
