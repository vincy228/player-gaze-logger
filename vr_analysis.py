import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="VR Log Viewer", layout="wide")
st.title("VR Log Viewer")

uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --- Detect existing time-like column ---
    time_columns = [c for c in df.columns if any(x in c.lower() for x in ["time", "timestamp", "frame"])]
    if not time_columns:
        st.error("❌ No time-related column found. Please include one (e.g., time, timestamp, frame_time).")
        st.stop()

    time_col = time_columns[0]
    timestamps = sorted(df[time_col].unique())

    # --- Separate static and dynamic ---
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]

    # --- Session state ---
    if "playing" not in st.session_state:
        st.session_state.playing = True
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "speed" not in st.session_state:
        st.session_state.speed = 1.0

    # --- Controls ---
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("⏯ Play / Pause"):
            st.session_state.playing = not st.session_state.playing

        st.session_state.speed = st.slider(
            "Playback Speed (×)", 0.25, 4.0, st.session_state.speed, 0.25
        )

    with c2:
        st.progress(st.session_state.idx / len(timestamps))

    # --- Placeholder for figure ---
    fig_placeholder = st.empty()

    # --- Playback loop ---
    start_real_time = time.time()
    start_log_time = timestamps[st.session_state.idx]

    while st.session_state.playing and st.session_state.idx < len(timestamps) - 1:
        elapsed_real = time.time() - start_real_time
        target_time = start_log_time + elapsed_real * st.session_state.speed

        # Move index forward based on time
        while (
            st.session_state.idx + 1 < len(timestamps)
            and timestamps[st.session_state.idx + 1] <= target_time
        ):
            st.session_state.idx += 1

        # --- Plot the current frame ---
        frame = dynamic_df[dynamic_df[time_col] == timestamps[st.session_state.idx]]
        fig, ax = plt.subplots()

        # Plot static trees
        ax.scatter(static_df["PosX"], static_df["PosZ"], c="green", marker="^", s=50, label="Tree")

        # Plot dynamic objects
        for cat in frame["Category"].unique():
            cat_data = frame[frame["Category"] == cat]
            color = "blue" if cat == "Player" else "red"
            marker = "o" if cat == "Player" else "s"
            size = 80 if cat == "Player" else 60
            ax.scatter(cat_data["PosX"], cat_data["PosZ"], c=color, marker=marker, s=size, label=cat)

        ax.set_title(f"Timestamp: {timestamps[st.session_state.idx]:.2f}")
        ax.set_xlabel("Unity X")
        ax.set_ylabel("Unity Z")
        ax.legend()
        fig_placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.05)  # control frame rate

    # --- End or pause behavior ---
    if st.session_state.idx >= len(timestamps) - 1:
        st.session_state.idx = 0
        st.session_state.playing = False
        fig_placeholder.info("🏁 Reached end of log — stopped.")
    elif not st.session_state.playing:
        fig_placeholder.info(f"⏸ Paused at frame {st.session_state.idx + 1}/{len(timestamps)}")

else:
    st.info("📁 Please upload your Unity log CSV to begin playback.")
