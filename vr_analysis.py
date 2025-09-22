import pandas as pd
import streamlit as st
import plotly.express as px

# Load CSV
df = pd.read_csv("vr_log.csv", sep="\t")  # <-- use sep="\t" if it's tab-delimited

# Show columns for debugging
st.write("CSV Columns:", df.columns.tolist())
st.write(df.head())

# Use correct column names
df["pos_x"] = df["PosX"]
df["pos_y"] = df["PosZ"]   # ignore Unity Y (use Z for 2D map)
df["time"] = df["Timestamp"]

# Plot 2D replay
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

fig.update_yaxes(scaleanchor="x", scaleratio=1)
st.plotly_chart(fig)
