import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

st.set_page_config(page_title="VR Log Viewer", layout="centered")
st.title("VR Log Viewer")

uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Separate static and dynamic
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]
    timestamps = sorted(dynamic_df["Timestamp"].unique())

    # --- Session state initialization ---
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "t_index" not in st.session_state:
        st.session_state.t_index = 0
    if "last_update" not in st.session_state:
        st.session_state.last_update = time.time()

    # --- UI Controls ---
    col1, col2 = st.columns([1, 4])
    with col1:
        play_label = "⏸️ Pause" if st.session_state.playing else "▶️ Play"
        if st.button(play_label):
            st.session_state.playing = not st.session_state.playing
            st.session_state.last_update = time.time()

    with col2:
        selected_t = st.slider(
            "Select Timestamp",
            min_value=float(min(timestamps)),
            max_value=float(max(timestamps)),
            value=float(timestamps[st.session_state.t_index]),
            step=0.01,
        )

    # --- Manual scrubbing when paused ---
    if not st.session_state.playing:
        st.session_state.t_index = min(
            range(len(timestamps)),
            key=lambda i: abs(timestamps[i] - selected_t)
        )

    # --- Auto advance if playing ---
    frame_interval = 0.2  # seconds between frames
    now = time.time()
    if st.session_state.playing and now - st.session_state.last_update > frame_interval:
        st.session_state.t_index += 1
        if st.session_state.t_index >= len(timestamps):
            st.session_state.t_index = 0  # loop to start
        st.session_state.last_update = now
        # Force re-render for the next frame
        st.experimental_rerun()

    # --- Draw current frame ---
    nearest_t = timestamps[st.session_state.t_index]
    frame = dynamic_df[dynamic_df["Timestamp"] == nearest_t]

    fig, ax = plt.subplots()
    ax.scatter(static_df["PosX"], static_df["PosZ"],
               c="green", marker="^", s=50, label="Tree")

    for cat in frame["Category"].unique():
        cat_data = frame[frame["Category"] == cat]
        color = "blue" if cat == "Player" else "red"
        marker = "o" if cat == "Player" else "s"
        size = 80 if cat == "Player" else 60
        ax.scatter(cat_data["PosX"], cat_data["PosZ"],
                   c=color, marker=marker, s=size, label=cat)

    ax.set_title(f"Timestamp: {nearest_t:.2f}")
    ax.set_xlabel("Unity X")
    ax.set_ylabel("Unity Z")
    ax.legend()
    st.pyplot(fig)
