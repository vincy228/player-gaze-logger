import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Sidebar upload ---
st.sidebar.header("Upload Logs")
player_file = st.sidebar.file_uploader("Upload Player.csv", type=["csv"])
objects_file = st.sidebar.file_uploader("Upload Objects.csv", type=["csv"])

if player_file and objects_file:
    # --- Load data ---
    player_df = pd.read_csv(player_file)
    objects_df = pd.read_csv(objects_file)

    st.subheader("Preview Data")
    st.write("**Player.csv**")
    st.dataframe(player_df.head())
    st.write("**Objects.csv**")
    st.dataframe(objects_df.head())

    # --- Create frames for animation ---
    frames = []
    unique_times = sorted(objects_df["time"].unique())

    for t in unique_times:
        frame_objects = objects_df[objects_df["time"] == t]
        frame_player = player_df[player_df["time"] == t]

        frame = go.Frame(
            data=[
                go.Scatter3d(
                    x=frame_objects["x"], y=frame_objects["y"], z=frame_objects["z"],
                    mode="markers",
                    marker=dict(size=4),
                    text=frame_objects["objectId"],
                    name="Objects"
                ),
                go.Scatter3d(
                    x=frame_player["x"], y=frame_player["y"], z=frame_player["z"],
                    mode="markers+lines",
                    marker=dict(size=6, color="red"),
                    line=dict(color="red", width=5),
                    name="Player"
                )
            ],
            name=str(t)
        )
        frames.append(frame)

    # --- Initial data (first frame) ---
    init_objects = objects_df[objects_df["time"] == unique_times[0]]
    init_player = player_df[player_df["time"] == unique_times[0]]

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=init_objects["x"], y=init_objects["y"], z=init_objects["z"],
                mode="markers",
                marker=dict(size=4),
                text=init_objects["objectId"],
                name="Objects"
            ),
            go.Scatter3d(
                x=init_player["x"], y=init_player["y"], z=init_player["z"],
                mode="markers+lines",
                marker=dict(size=6, color="red"),
                line=dict(color="red", width=5),
                name="Player"
            )
        ],
        layout=go.Layout(
            title="Player & Objects Animation",
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                        "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                          "mode": "immediate",
                                          "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "steps": [
                    {
                        "args": [[str(t)], {"frame": {"duration": 0, "redraw": True},
                                            "mode": "immediate",
                                            "transition": {"duration": 0}}],
                        "label": str(t),
                        "method": "animate"
                    }
                    for t in unique_times
                ],
                "x": 0.1,
                "len": 0.9,
                "xanchor": "left",
                "y": -0.05,
                "yanchor": "top"
            }]
        ),
        frames=frames
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload both **Player.csv** and **Objects.csv** to start.")