import pandas as pd
import streamlit as st
import plotly.express as px

st.title("VR Session Replay (Top-down XZ)")

uploaded_file = st.file_uploader("Upload VR log CSV", type=["csv"])

if uploaded_file is not None:
    # Try reading tab-delimited first
    try:
        df = pd.read_csv(uploaded_file, sep="\t")
    except:
        df = pd.read_csv(uploaded_file)

    st.write("Preview of CSV:", df.head())  # Debugging preview

    # Clean column names
    df.columns = df.columns.str.strip()

    # Extract unique timestamps
    timestamps = sorted(df["Timestamp"].unique())

    # Separate static trees
    tree_df = df[df["Category"] == "Tree"]

    # Duplicate tree rows across all timestamps
    expanded_trees = pd.concat(
        [tree_df.assign(Timestamp=t) for t in timestamps],
        ignore_index=True
    )

    # Keep dynamic/player objects separate
    moving_df = df[df["Category"] != "Tree"]

    # Combine back
    final_df = pd.concat([moving_df, expanded_trees], ignore_index=True)

    # Add XZ projection
    final_df["pos_x"] = final_df["PosX"]
    final_df["pos_z"] = final_df["PosZ"]

    # Use timestamp as string for animation frames
    final_df["time"] = final_df["Timestamp"].astype(str)

    # Animated 2D scatter plot
    fig = px.scatter(
        final_df,
        x="pos_x",
        y="pos_z",
        animation_frame="time",
        animation_group="ObjectName",
        color="Category",
        hover_name="ObjectName",
        title="VR Replay (Top-down XZ)"
    )

    # Keep map aspect ratio square
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    st.plotly_chart(fig, use_container_width=True)
