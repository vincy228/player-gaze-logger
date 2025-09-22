import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title("🎬 VR Session Replay")

uploaded_file = st.file_uploader("Upload VR Log CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.write(df.head())

    # Separate static vs dynamic
    trees = df[df["Category"] == "Tree"].drop_duplicates(subset=["ObjectName"])
    moving = df[df["Category"] != "Tree"]

    # All unique timestamps (sorted)
    timestamps = sorted(moving["Timestamp"].unique())

    # Session state
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Play"):
            st.session_state.is_playing = True
    with col2:
        if st.button("⏸️ Pause"):
            st.session_state.is_playing = False

    # Playback speed
    step_time = st.sidebar.slider("Playback speed (seconds per frame)", 0.1, 2.0, 0.5, 0.1)

    # Timeline scrubber
    st.session_state.current_index = st.slider(
        "Scrub timeline",
        0, len(timestamps)-1,
        st.session_state.current_index,
        1
    )

    # Function to plot single frame
    def plot_frame(index):
        t = timestamps[index]
        frame_df = moving[moving["Timestamp"] == t]
        combined_df = pd.concat([frame_df, trees], ignore_index=True)

        fig = px.scatter_3d(
            combined_df,
            x="PosX", y="PosY", z="PosZ",
            color="Category",
            symbol="Category",
            hover_data=["ObjectName", "Category"],
            title=f"Time {t:.2f}s"
        )
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

    # Manual mode (pause)
    if not st.session_state.is_playing:
        plot_frame(st.session_state.current_index)

    # Auto mode (play)
    if st.session_state.is_playing:
        for i in range(st.session_state.current_index, len(timestamps)):
            if not st.session_state.is_playing:
                break
            st.session_state.current_index = i
            plot_frame(i)
            time.sleep(step_time)
