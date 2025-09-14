import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("VR Player Movement Viewer")

# Upload CSV
uploaded_file = st.file_uploader("Upload player_log.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Project onto X-Z plane
    df["x"] = df["x"] - df["x"].min()
    df["z"] = df["z"] - df["z"].min()

    # Time selection slider
    i = st.slider("Select time index", 0, len(df)-1, 0)

    # Plot at selected time
    fig, ax = plt.subplots()
    ax.plot(df["x"][:i], df["z"][:i], "b-", alpha=0.6)  # path up to time
    ax.scatter(df["x"].iloc[i], df["z"].iloc[i], c="red", s=50)  # current position
    ax.set_xlabel("X position")
    ax.set_ylabel("Z position")
    ax.set_title("Player Path (Top-Down)")
    st.pyplot(fig)

    # Show current time
    st.metric("Current Time", f"{df['time'].iloc[i]:.2f} sec")