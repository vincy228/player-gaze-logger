import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title("VR Session Replay")

uploaded_file = st.file_uploader("Upload the VR log CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Separate categories
    player_df = df[df["Category"] == "Player"]
    elephant_df = df[df["Category"] == "Elephant"]
    tree_df = df[df["Category"] == "Tree"].drop_duplicates(subset=["ObjectName"])

    timestamps = sorted(player_df["Timestamp"].unique())
    min_t, max_t = min(timestamps), max(timestamps)

    # Sidebar controls
    step = st.sidebar.slider("Playback speed (seconds per frame)", 0.1, 2.0, 0.5, 0.1)

    # Session state
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "current_t" not in st.session_state:
        st.session_state.current_t = min_t

    # Timeline scrubber
    selected_t = st.slider("Scrub timeline", min_value=float(min_t), max_value=float(max_t),
                           value=float(st.session_state.current_t), step=1.0)

    def plot_frame(t):
        frame_df = df[df["Timestamp"] == t]
        combined_df = pd.concat([frame_df, tree_df], ignore_index=True)

        fig = px.scatter_3d(
            combined_df,
            x="PosX", y="PosY", z="PosZ",
            color="Category",
            symbol="Category",
            hover_data=["ObjectName", "Timestamp"],
            title=f"Time {t:.2f}s"
        )

        # Custom symbols for categories
        fig.update_traces(marker=dict(size=6))
        fig.update_traces(selector=dict(mode="markers"))
        fig.update_layout(
            legend=dict(title="Category"),
        )
        fig.update_traces(marker_symbol="circle", selector=dict(name="Player"))
        fig.update_traces(marker_symbol="square", selector=dict(name="Elephant"))
        fig.update_traces(marker_symbol="diamond", selector=dict(name="Tree"))

        st.plotly_chart(fig, use_container_width=True)

    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play"):
            st.session_state.is_playing = True
    with col2:
        if st.button("Pause"):
            st.session_state.is_playing = False

    # Manual scrubbing
    if not st.session_state.is_playing:
        st.session_state.current_t = selected_t
        plot_frame(st.session_state.current_t)

    # Auto playback
    if st.session_state.is_playing:
        for t in timestamps:
            if not st.session_state.is_playing:
                break
            st.session_state.current_t = t
            plot_frame(t)
            time.sleep(step)