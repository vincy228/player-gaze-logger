import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.title("VR Log Viewer")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Prepare data ---
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]
    timestamps = sorted(dynamic_df["Timestamp"].unique())

    # --- Initialize playback state ---
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = True  # autoplay on load
    if "timestamp_index" not in st.session_state:
        st.session_state.timestamp_index = 0

    # --- Placeholders for UI ---
    plot_placeholder = st.empty()

    # --- Play / Pause toggle ---
    def toggle_play():
        # Toggle play/pause
        st.session_state.is_playing = not st.session_state.is_playing
        # Restart from beginning if reached end
        if st.session_state.timestamp_index >= len(timestamps) - 1:
            st.session_state.timestamp_index = 0

    play_label = "⏸ Pause" if st.session_state.is_playing else "▶ Play"
    st.button(play_label, on_click=toggle_play)

    # --- Function to render frame ---
    def render_frame(idx):
        nearest_t = timestamps[idx]
        frame = dynamic_df[dynamic_df["Timestamp"] == nearest_t]

        fig, ax = plt.subplots()
        ax.scatter(static_df["PosX"], static_df["PosZ"], c="green", marker="^", s=50, label="Tree")

        for cat in frame["Category"].unique():
            cat_data = frame[frame["Category"] == cat]
            color = "blue" if cat == "Player" else "red"
            marker = "o" if cat == "Player" else "s"
            size = 80 if cat == "Player" else 60
            ax.scatter(cat_data["PosX"], cat_data["PosZ"], c=color, marker=marker, s=size, label=cat)

        ax.set_title(f"Timestamp: {nearest_t:.2f}")
        ax.set_xlabel("Unity X")
        ax.set_ylabel("Unity Z")
        ax.legend()
        plot_placeholder.pyplot(fig)
        plt.close(fig)

    # --- Playback loop ---
    if st.session_state.is_playing:
        for i in range(st.session_state.timestamp_index, len(timestamps)):
            if not st.session_state.is_playing:
                break
            st.session_state.timestamp_index = i
            render_frame(i)
            time.sleep(0.05)

        # --- When reach end, stop and wait for user ---
        if st.session_state.timestamp_index >= len(timestamps) - 1:
            st.session_state.is_playing = False
            st.session_state.timestamp_index = 0  # ready for replay
    else:
        render_frame(st.session_state.timestamp_index)
