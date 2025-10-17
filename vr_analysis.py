import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

st.title("VR Log Viewer")

# --- Upload CSV file ---
uploaded_file = st.file_uploader("Upload your Unity log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Separate static and dynamic objects ---
    static_df = df[df["Category"] == "Tree"]
    dynamic_df = df[df["Category"] != "Tree"]

    # --- Extract timestamps ---
    timestamps = sorted(dynamic_df["Timestamp"].unique())

    # --- Initialize session state ---
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "t_index" not in st.session_state:
        st.session_state.t_index = 0

    # --- Play / Pause button ---
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.session_state.playing:
            if st.button("⏸️ Pause"):
                st.session_state.playing = False
        else:
            if st.button("▶️ Play"):
                st.session_state.playing = True

    # --- Manual timestamp slider ---
    with col2:
        selected_t = st.slider(
            "Select Timestamp",
            min_value=float(min(timestamps)),
            max_value=float(max(timestamps)),
            value=float(timestamps[st.session_state.t_index]),
            step=0.01
        )

    # --- Update timestamp index when slider moves ---
    st.session_state.t_index = min(
        range(len(timestamps)),
        key=lambda i: abs(timestamps[i] - selected_t)
    )

    # --- Handle playback loop ---
    if st.session_state.playing:
        placeholder = st.empty()
        for i in range(st.session_state.t_index, len(timestamps)):
            if not st.session_state.playing:
                break
            st.session_state.t_index = i
            nearest_t = timestamps[i]

            with placeholder.container():
                fig, ax = plt.subplots()

                # Static (trees)
                ax.scatter(static_df["PosX"], static_df["PosZ"],
                           c="green", marker="^", s=50, label="Tree")

                # Dynamic at this frame
                frame = dynamic_df[dynamic_df["Timestamp"] == nearest_t]
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

            time.sleep(0.2)  # Adjust playback speed

        st.session_state.playing = False

    else:
        # --- Static display (manual mode) ---
        nearest_t = timestamps[st.session_state.t_index]
        fig, ax = plt.subplots()

        ax.scatter(static_df["PosX"], static_df["PosZ"],
                   c="green", marker="^", s=50, label="Tree")

        frame = dynamic_df[dynamic_df["Timestamp"] == nearest_t]
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
