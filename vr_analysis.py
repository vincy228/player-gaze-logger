import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

# Load CSV
df = pd.read_csv("your_log.csv")

# Separate static and dynamic
static_df = df[df["Category"] == "Tree"]
dynamic_df = df[df["Category"] != "Tree"]

# Get unique timestamps
timestamps = sorted(dynamic_df["Timestamp"].unique())

# Create Streamlit figure
plot_spot = st.empty()

for t in timestamps:
    fig, ax = plt.subplots()

    # --- Static objects (trees) ---
    ax.scatter(static_df["PosX"], static_df["PosZ"], c="green", marker="^", s=50, label="Tree")

    # --- Dynamic objects (player, elephants, etc.) ---
    frame = dynamic_df[dynamic_df["Timestamp"] == t]
    for cat in frame["Category"].unique():
        cat_data = frame[frame["Category"] == cat]
        if cat == "Player":
            ax.scatter(cat_data["PosX"], cat_data["PosZ"], c="blue", marker="o", s=80, label="Player")
        else:
            ax.scatter(cat_data["PosX"], cat_data["PosZ"], c="red", marker="s", s=60, label=cat)

    ax.set_title(f"Timestamp: {t:.2f}")
    ax.set_xlabel("Unity X")
    ax.set_ylabel("Unity Z")
    ax.legend()

    plot_spot.pyplot(fig)
    plt.close(fig)
    time.sleep(0.2)  # Controls animation speed
