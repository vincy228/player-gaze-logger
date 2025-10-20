import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="VR Log Player", layout="wide")

uploaded_file = st.file_uploader("Upload Unity Log CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --- Detect existing time-like column without renaming ---
    time_columns = [c for c in df.columns if any(x in c.lower() for x in ["time", "timestamp", "frame"])]
    if not time_columns:
        st.error("❌ No time-related column found. Please include one (e.g., time, timestamp, frame_time).")
        st.stop()

    # Use the first matching column as the time reference
    time_col = time_columns[0]
    timestamps = df[time_col].values
    st.write(f"🕒 Using time column: **{time_col}** ({len(timestamps)} entries)")

    # --- Session State ---
    if "playing" not in st.session_state:
        st.session_state.playing = True  # auto-play
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

    # --- Display placeholder ---
    placeholder = st.empty()

    # --- Playback loop ---
    start_real_time = time.time()
    start_log_time = timestamps[st.session_state.idx]

    while st.session_state.playing and st.session_state.idx < len(timestamps) - 1:
        elapsed_real = time.time() - start_real_time
        target_time = start_log_time + elapsed_real * st.session_state.speed

        # Advance index while log time ≤ target time
        while (
            st.session_state.idx + 1 < len(timestamps)
            and timestamps[st.session_state.idx + 1] <= target_time
        ):
            st.session_state.idx += 1

        # Update display (you can replace this with your plot update)
        placeholder.write(f"🎮 Playing frame {st.session_state.idx + 1}/{len(timestamps)}")

        time.sleep(0.02)

    # --- End or pause behavior ---
    if st.session_state.idx >= len(timestamps) - 1:
        st.session_state.idx = 0
        st.session_state.playing = False
        placeholder.write("🏁 Reached end of log — stopped.")
    elif not st.session_state.playing:
        placeholder.write(f"⏸ Paused at frame {st.session_state.idx + 1}/{len(timestamps)}")

else:
    st.info("📁 Please upload your Unity log CSV to begin playback.")
