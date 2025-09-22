import pandas as pd
import streamlit as st
import plotly.express as px

st.title("VR Session Replay (2D)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload VR log CSV", type=["csv"])

if uploaded_file is not None:
    # Read uploaded CSV (try comma first, then tab)
    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file, sep="\t")

    # Show columns for debugging
    st.write("CSV Columns:", df.columns.tolist())
    st.write(df.head())

    # Normalize column names
    df["pos_x"] = df["PosX"]
    df["pos_y"] = df["PosZ"]   # ignore Unity Y, use Z
    df["time"] = df["Timestamp"]

    # 2D animated scatter plot
    fig = px.scatter(
        df,
        x="pos_x",
        y="pos_y",
        animation_frame="time",
        animation_group="ObjectName",
        color="Category",
        hover_name="ObjectName",
        title="VR Replay (2D)"
    )

    # Keep aspect ratio equal
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    st.plotly_chart(fig, use_container_width=True)
