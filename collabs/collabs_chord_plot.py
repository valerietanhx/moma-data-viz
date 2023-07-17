import math

import holoviews as hv
import numpy as np
import pandas as pd
from bokeh.plotting import show

hv.extension("bokeh")
hv.output(size=200)

edges = pd.read_csv("collabs/CollabsGraphEdges.csv")
edges = edges.query("`value` >= 20")  # avoid plot looking like a yarn ball
unique_nationalities_edges = pd.concat([edges["source"], edges["target"]]).unique()

selection = pd.read_csv("collabs/CollabsSelectionEdges.csv")
selection = selection[
    selection["source"].isin(unique_nationalities_edges)
    & selection["target"].isin(unique_nationalities_edges)
][["source", "value"]]
nationality_freq = selection.groupby("source").sum().reset_index()
nationality_freq = nationality_freq.rename(
    columns={"source": "Nationality", "value": "Total Count"}
)

nationality_freq = hv.Dataset(nationality_freq, "Nationality")
chord = hv.Chord((edges, nationality_freq))


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
    cmap="Set3",
    edge_cmap="Set3",
    edge_color="source",
    labels="Nationality",
    node_color="Nationality",
    hooks=[rotate_label],
)

show(hv.render(chord))
