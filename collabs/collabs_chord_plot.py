import math

import holoviews as hv
import numpy as np
import pandas as pd
from bokeh.plotting import show
from holoviews import dim

hv.extension("bokeh")
hv.output(size=200)

edges = pd.read_csv("collabs/CollabsGraphEdgesV2.csv")
edges = edges.query("`value` >= 20")  # avoid plot looking like a yarn ball

chord = hv.Chord((edges))

# https://stackoverflow.com/questions/65561927/inverted-label-text-half-turn-for-chord-diagram-on-holoviews-with-bokeh/65610161#65610161
def rotate_label(plot, element):
    whitespace = " " * 16
    angles = plot.handles["text_1_source"].data["angle"]
    chars = np.array(plot.handles["text_1_source"].data["text"])
    plot.handles["text_1_source"].data["text"] = np.array(
        [
            x + whitespace
            if x in chars[np.where((angles < -math.pi / 2) | (angles > math.pi / 2))]
            else x
            for x in plot.handles["text_1_source"].data["text"]
        ]
    )
    plot.handles["text_1_source"].data["text"] = np.array(
        [
            whitespace + x
            if x in chars[np.where((angles > -math.pi / 2) | (angles < math.pi / 2))]
            else x
            for x in plot.handles["text_1_source"].data["text"]
        ]
    )
    angles[np.where((angles < -math.pi / 2) | (angles > math.pi / 2))] += math.pi
    plot.handles["text_1_glyph"].text_align = "center"

chord.opts(
    cmap="Category20",
    edge_cmap="Category20",
    edge_color=dim("source").str(),
    labels="index",
    node_color=dim("index").str(),
    hooks=[rotate_label],
)


show(hv.render(chord))
