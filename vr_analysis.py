import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("vr_log.csv")

# Flatten Unity’s (X,Z), ignore Y
df["pos_x"] = df["pos_x"]
df["pos_y"] = df["pos_z"]   # use Z as Y in 2D map

# Optional: make labels cleaner
df["object"] = df["object"].astype(str)

# Animated scatter in 2D
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

# Fix aspect ratio so distances are preserved
fig.update_layout(
    yaxis=dict(scaleanchor="x", scaleratio=1),
    width=800,
    height=800
)

st.plotly_chart(fig)
