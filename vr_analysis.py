import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

st.title("VR Log Viewer")

uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Separate static and dynamic
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]

    timestamps = sorted(dynamic_df["Timestamp"].unique())

    # --- Initialize session state ---
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "t_index" not in st.session_state:
        st.session_state.t_index = 0

    # --- Control buttons and slider ---
    col1, col2 = st.columns([1, 4])

    with col1:
        if st.session_state.playing:
            if st.button("⏸️ Pause", key="pause_btn"):
                st.session_state.playing = False
        else:
            if st.button("▶️ Play", key="play_btn"):
                st.session_state.playing = True

    with col2:
        selected_t = st.slider(
            "Select Timestamp",
            min_value=float(min(timestamps)),
            max_value=float(max(timestamps)),
            value=float(timestamps[st.session_state.t_index]),
            step=0.01,
            key="timestamp_slider"
        )

    # Sync t_index if user manually scrubs
    st.session_state.t_index = min(
        range(len(timestamps)),
        key=lambda i: abs(timestamps[i] - selected_t)
    )

    # --- Placeholder for live plot ---
    placeholder = st.empty()

    # --- Main drawing function ---
    def draw_frame(index):
        nearest_t = timestamps[index]
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
        placeholder.pyplot(fig)

    # --- Handle playback loop ---
    if st.session_state.playing:
        for i in range(st.session_state.t_index, len(timestamps)):
            if not st.session_state.playing:
                break

            st.session_state.t_index = i
            draw_frame(i)

            # Move slider visually (forces rerun)
            st.session_state.timestamp_slider = float(timestamps[i])

            time.sleep(0.2)
            st.rerun()

    # --- Manual view when not playing ---
    else:
        draw_frame(st.session_state.t_index)
