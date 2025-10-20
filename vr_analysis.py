import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="VR Gaze Playback", layout="wide")

uploaded_file = st.file_uploader("Upload gaze log CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'timestamp' not in df.columns:
        st.error("CSV must contain a 'timestamp' column.")
    else:
        timestamps = df['timestamp'].values
        st.write(f"Loaded {len(timestamps)} frames from log file.")

        # Initialize session state
        if "playing" not in st.session_state:
            st.session_state.playing = True
        if "current_idx" not in st.session_state:
            st.session_state.current_idx = 0
        if "play_speed" not in st.session_state:
            st.session_state.play_speed = 1.0  # multiplier, not delay

        # Controls
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("⏯ Play / Pause"):
                st.session_state.playing = not st.session_state.playing

            st.session_state.play_speed = st.slider(
                "Playback Speed (×)", 0.25, 4.0, st.session_state.play_speed, 0.25
            )

        with col2:
            st.progress(st.session_state.current_idx / len(timestamps))

        placeholder = st.empty()

        start_time = time.time()
        start_timestamp = timestamps[st.session_state.current_idx]

        while st.session_state.playing and st.session_state.current_idx < len(timestamps):
            elapsed_real_time = time.time() - start_time
            target_timestamp = start_timestamp + elapsed_real_time * st.session_state.play_speed

            # Find the closest frame that matches playback time
            while (
                st.session_state.current_idx + 1 < len(timestamps)
                and timestamps[st.session_state.current_idx + 1] <= target_timestamp
            ):
                st.session_state.current_idx += 1

            # Display frame content
            placeholder.write(f"🎯 Frame {st.session_state.current_idx+1}/{len(timestamps)}")

            # Check end
            if st.session_state.current_idx >= len(timestamps) - 1:
                st.session_state.playing = False
                st.session_state.current_idx = 0
                st.experimental_rerun()

            time.sleep(0.02)  # refresh 50 FPS for smoothness

        if not st.session_state.playing:
            placeholder.write(f"⏸ Paused at frame {st.session_state.current_idx+1}/{len(timestamps)}")
else:
    st.info("Please upload a log file to begin playback.")
