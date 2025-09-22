import pandas as pd
import streamlit as st
import plotly.express as px

st.title("VR Session Replay (Top-down 2D)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload VR log CSV", type=["csv"])

if uploaded_file is not None:
    # Read uploaded CSV (comma first, then tab)
    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file, sep="\t")

    # Show CSV columns for debugging
    st.write("CSV Columns:", df.columns.tolist())
    st.write(df.head())

    # Use Unity X and Z (ignore Y)
    df["pos_x"] = df["PosX"]
    df["pos_z"] = df["PosZ"]   # Z is depth

    df["time"] = df["Timestamp"]

    # Animated 2D scatter (top-down map)
    fig = px.scatter(
        df,
        x="pos_x",
        y="pos_z",
        animation_frame="time",
        animation_group="ObjectName",
        color="Category",
        hover_name="ObjectName",
        title="VR Replay (Top-down XZ view)"
    )

    # Keep aspect ratio equal
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    st.plotly_chart(fig, use_container_width=True)
