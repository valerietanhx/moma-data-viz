import math
import os

import holoviews as hv
import numpy as np
import pandas as pd
from bokeh.plotting import show
from holoviews import dim

hv.extension("bokeh")
hv.output(size=200)

CURR_FILEPATH = os.path.dirname(__file__)

collabs_graph_edges_path = os.path.join(CURR_FILEPATH, "CollabsGraphEdges.csv")
edges = pd.read_csv(collabs_graph_edges_path)
edges = edges.query("`value` >= 18")  # avoid plot looking like a yarn ball
# only 49 out of 481 collaborations between nationalities occured >= 18 times!
# that's a fact to visualise

edge_indexes = (
    pd.concat([edges["source"], edges["target"]])
    .drop_duplicates()
    .to_frame(name="edge_index")
)


collabs_graph_nodes_path = os.path.join(CURR_FILEPATH, "CollabsGraphNodes.csv")
nodes = pd.read_csv(collabs_graph_nodes_path)
nodes = nodes.merge(edge_indexes, how="right", left_on="index", right_on="edge_index")
nodes.drop("edge_index", axis=1, inplace=True)
nodes = hv.Dataset(nodes, "index")

chord = hv.Chord((edges, nodes))


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
    labels="nationality",
    node_color=dim("index").str(),
    hooks=[rotate_label],
)


show(hv.render(chord))  # automatically saves collabs_plot.html in same directory
