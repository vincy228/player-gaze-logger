import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎬 VR Session Replay (Single Animated Visual)")

uploaded_file = st.file_uploader("Upload VR Log CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.write(df.head())

    # Separate static vs dynamic
    trees = df[df["Category"] == "Tree"].drop_duplicates(subset=["ObjectName"])
    moving = df[df["Category"] != "Tree"]

    # Ensure trees appear in every animation frame (fixed background)
    timestamps = moving["Timestamp"].unique()
    trees_expanded = pd.DataFrame([
        {
            "Timestamp": t,
            "ObjectName": row.ObjectName,
            "PosX": row.PosX,
            "PosY": row.PosY,
            "PosZ": row.PosZ,
            "Category": row.Category
        }
        for t in timestamps
        for _, row in trees.iterrows()
    ])

    # Merge back together
    full_df = pd.concat([moving, trees_expanded], ignore_index=True)

    # Create single animated 3D scatter
    fig = px.scatter_3d(
        full_df,
        x="PosX", y="PosY", z="PosZ",
        color="Category",
        symbol="Category",
        animation_frame="Timestamp",   # <-- drives animation
        animation_group="ObjectName",  # <-- keeps same object moving
        hover_data=["ObjectName", "Category"],
        title="VR Replay (Single Animated Visual)"
    )

    # Adjust visuals
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
        legend=dict(title="Object Type")
    )

    # Display interactive animated chart (with Play/Pause + scrub bar)
    st.plotly_chart(fig, use_container_width=True)
