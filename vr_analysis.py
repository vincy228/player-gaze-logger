import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎬 VR Session Replay (Fixed Multiple Objects)")

uploaded_file = st.file_uploader("Upload VR Log CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.write(df.head())

    # ✅ Make sure each object has a unique ID
    df["ObjectID"] = df.groupby("ObjectName").cumcount().astype(str)
    df["UniqueName"] = df["ObjectName"] + "_" + df["ObjectID"]

    # Separate static and dynamic
    trees = df[df["Category"] == "Tree"]
    moving = df[df["Category"] != "Tree"]

    # Ensure trees appear in every frame (so they stay visible)
    timestamps = moving["Timestamp"].unique()
    trees_expanded = pd.DataFrame([
        {
            "Timestamp": t,
            "ObjectName": row.ObjectName,
            "UniqueName": row.UniqueName,
            "PosX": row.PosX,
            "PosY": row.PosY,
            "PosZ": row.PosZ,
            "Category": row.Category
        }
        for t in timestamps
        for _, row in trees.iterrows()
    ])

    # Merge back
    full_df = pd.concat([moving, trees_expanded], ignore_index=True)

    # ✅ Use UniqueName to keep each tree/elephant separate
    fig = px.scatter_3d(
        full_df,
        x="PosX", y="PosY", z="PosZ",
        color="Category",
        symbol="Category",
        animation_frame="Timestamp",
        animation_group="UniqueName",
        hover_data=["ObjectName", "Category"],
        title="VR Replay (All Objects)"
    )

    # Tweak visuals
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
        legend=dict(title="Object Type")
    )

    st.plotly_chart(fig, use_container_width=True)
