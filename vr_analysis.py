import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.title("VR Log Viewer")

uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Separate static and dynamic ---
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]
    timestamps = sorted(dynamic_df["Timestamp"].unique())

    # --- Initialize playback state ---
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = True  # autoplay
    if "timestamp_index" not in st.session_state:
        st.session_state.timestamp_index = 0

    # --- Play / Pause button ---
    def toggle_play():
        st.session_state.is_playing = not st.session_state.is_playing

    play_label = "⏸ Pause" if st.session_state.is_playing else "▶ Play"
    st.button(play_label, on_click=toggle_play)

    # --- Style map ---
    style_map = {
        "Player": ("blue", "o", 80),       # blue circle
        "Elephants": ("orange", "s", 70),  # orange square
        "Tree": ("green", "^", 50)         # green triangle
    }

    # --- Render frame ---
    idx = st.session_state.timestamp_index
    nearest_t = timestamps[idx]
    frame = dynamic_df[dynamic_df["Timestamp"] == nearest_t]

    fig, ax = plt.subplots()

    # Draw static trees
    if not static_df.empty:
        color, marker, size = style_map["Tree"]
        ax.scatter(static_df["PosX"], static_df["PosZ"], c=color, marker=marker, s=size, label="Tree")

    # Draw dynamic objects
    for cat in frame["Category"].unique():
        cat_data = frame[frame["Category"] == cat]
        if cat in style_map:
            color, marker, size = style_map[cat]
        else:
            color, marker, size = ("red", "x", 60)
        ax.scatter(cat_data["PosX"], cat_data["PosZ"], c=color, marker=marker, s=size, label=cat)

    ax.set_title(f"Timestamp: {nearest_t:.2f}")
    ax.set_xlabel("Unity X")
    ax.set_ylabel("Unity Z")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    # --- Playback control ---
    if st.session_state.is_playing:
        time.sleep(0.05)
        st.session_state.timestamp_index += 1
        if st.session_state.timestamp_index >= len(timestamps):
            st.session_state.timestamp_index = 0  # auto-loop
        st.rerun()
