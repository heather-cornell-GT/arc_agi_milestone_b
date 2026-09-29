# arc_viewer_flexible.py
# Supports both ARC JSON files and direct list of numpy ndarrays

import json
import webbrowser
import tempfile
import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from tkinter import filedialog

# ARC color palette
arc_hex = [
    '#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
    '#A0A0A0', '#F012BE', '#FF851B', '#7FDBFF', '#870C25',
]
colorscale = [[i / 9.0, color] for i, color in enumerate(arc_hex)]


# ────────────────────────────────────────────────
def load_arc_task(file_path):
    """Load training and test grids from ARC JSON"""
    with open(file_path, 'r') as f:
        data = json.load(f)

    train_inputs = [np.array(ex["input"], dtype=int) for ex in data.get("train", [])]
    train_outputs = [np.array(ex["output"], dtype=int) for ex in data.get("train", [])]

    test_inputs = [np.array(ex["input"], dtype=int) for ex in data.get("test", [])]
    test_outputs = []
    for ex in data.get("test", []):
        if "output" in ex and ex["output"] is not None:
            test_outputs.append(np.array(ex["output"], dtype=int))
        else:
            test_outputs.append(None)

    return train_inputs, train_outputs, test_inputs, test_outputs


# ────────────────────────────────────────────────
def display_grids(grids_list, title="Custom Grid Collection", cell_px=42):
    """
    Display a list of numpy ndarrays in the same clean style.

    Parameters:
        grids_list: list of np.ndarray (each is a 2D grid with values 0-9)
        title:      window title / figure title
        cell_px:    base size of one grid cell in pixels
    """
    if not grids_list:
        print("No grids provided.")
        return

    n_grids = len(grids_list)
    cols = 1
    rows = n_grids

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"Grid {i + 1}" for i in range(n_grids)],
        vertical_spacing=0.06,
    )

    for i, grid in enumerate(grids_list):
        h, w = grid.shape
        fig.add_trace(
            go.Heatmap(
                z=grid,
                colorscale=colorscale,
                zmin=0, zmax=9,
                showscale=False,
                xgap=2, ygap=2,
                hoverongaps=False,
                hovertemplate="%{z}<extra></extra>"
            ),
            row=i + 1, col=1
        )
        fig.update_xaxes(row=i + 1, col=1, range=[-0.5, w - 0.5])
        fig.update_yaxes(row=i + 1, col=1, range=[h - 0.5, -0.5])

    # Uniform cell size
    max_w = max(g.shape[1] for g in grids_list)
    max_h = max(g.shape[0] for g in grids_list)

    fig_width = cols * (max_w * cell_px + 100)
    fig_height = rows * (max_h * cell_px + 60) + 100

    fig.update_layout(
        title_text=title,
        title_x=0.5,
        height=fig_height,
        width=fig_width,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f8f8f8",
        margin=dict(l=60, r=60, t=80, b=40),
        font=dict(family="Arial", size=13),
        showlegend=False
    )

    for r in range(1, rows + 1):
        fig.update_xaxes(row=r, col=1,
                         scaleanchor="y", scaleratio=1,
                         showticklabels=False, ticks="", zeroline=False, showgrid=False)
        fig.update_yaxes(row=r, col=1,
                         scaleanchor="x", scaleratio=1,
                         showticklabels=False, ticks="", zeroline=False, showgrid=False)

    # Save & open
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        path = tmp.name
        fig.write_html(path, include_plotlyjs='cdn', full_html=True,
                       config={'responsive': True})

    print(f"Opening custom grids viewer: {path}")
    webbrowser.open(f"file://{os.path.abspath(path)}")


# ────────────────────────────────────────────────
def main():
    print("ARC Grid Viewer")
    print("1 = Load ARC JSON file")
    print("2 = Display list of numpy arrays (example/demo mode)")
    choice = input("Choose mode (1 or 2): ").strip()

    if choice == "1":
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Select ARC task JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            print("No file selected.")
            return

        train_in, train_out, test_in, test_out = load_arc_task(file_path)

        # Prepare grids list (flattened)
        grids = []
        labels = []

        for i in range(len(train_in)):
            grids.append(train_in[i])
            labels.append(f"Train {i + 1} Input")
            grids.append(train_out[i])
            labels.append(f"Train {i + 1} Output")

        for i, (tin, tout) in enumerate(zip(test_in, test_out)):
            grids.append(tin)
            labels.append(f"Test {i + 1} Input")
            if tout is not None:
                grids.append(tout)
                labels.append(f"Test {i + 1} Output")

        # Display with labels
        display_grids(grids, title=f"ARC Task: {os.path.basename(file_path)}", cell_px=42)

    elif choice == "2":
        # Example: your own list of grids You can change this out for your own
        example_grids = [
            np.random.randint(0, 10, (5, 5)),
            np.random.randint(0, 10, (3, 7)),
            np.random.randint(0, 10, (8, 4)),
            np.ones((6, 6), int) * 4,
        ]

        print("Displaying example list of 4 random grids...")
        display_grids(example_grids, title="Custom List of Grids", cell_px=45)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()