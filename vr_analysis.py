import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="VR Gaze Playback", layout="wide")

# --- Load your log file ---
# Replace with your actual CSV path or uploader
uploaded_file = st.file_uploader("Upload gaze log CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'timestamp' not in df.columns:
        st.error("CSV must contain a 'timestamp' column.")
    else:
        timestamps = df['timestamp'].values
        st.write(f"Loaded {len(timestamps)} frames from log file.")

        # --- Playback controls ---
        col1, col2 = st.columns([1, 3])
        with col1:
            if "playing" not in st.session_state:
                st.session_state.playing = True
            if "current_idx" not in st.session_state:
                st.session_state.current_idx = 0
            if "play_speed" not in st.session_state:
                st.session_state.play_speed = 1.0  # seconds per step

            if st.button("⏯ Play / Pause"):
                st.session_state.playing = not st.session_state.playing

            st.session_state.play_speed = st.slider("Play speed (s/step)", 0.05, 1.0, st.session_state.play_speed, 0.05)

        with col2:
            st.progress(st.session_state.current_idx / len(timestamps))

        # --- Playback loop ---
        placeholder = st.empty()

        while st.session_state.playing:
            current_idx = st.session_state.current_idx

            # Stop at end and auto-reset
            if current_idx >= len(timestamps):
                st.session_state.playing = False
                st.session_state.current_idx = 0
                st.experimental_rerun()

            # Simulated "frame display"
            placeholder.write(f"🎯 Frame {current_idx + 1}/{len(timestamps)} — Timestamp: {timestamps[current_idx]:.2f}")

            # Next frame
            st.session_state.current_idx += 1

            time.sleep(st.session_state.play_speed)

        # When paused, show current frame
        if not st.session_state.playing and st.session_state.current_idx < len(timestamps):
            placeholder.write(f"⏸ Paused at frame {st.session_state.current_idx + 1}/{len(timestamps)}")

else:
    st.info("Please upload a log file to begin playback.")
