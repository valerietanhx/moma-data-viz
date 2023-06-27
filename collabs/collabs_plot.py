import os

import holoviews as hv
import pandas as pd

# from bokeh.plotting import show
from holoviews import dim, opts

hv.extension("bokeh")
hv.output(size=200)

CURR_FILEPATH = os.path.dirname(__file__)

collabs_graph_edges_path = os.path.join(CURR_FILEPATH, "CollabsGraphEdges.csv")
edges = pd.read_csv(collabs_graph_edges_path)

collabs_graph_nodes_path = os.path.join(CURR_FILEPATH, "CollabsGraphNodes.csv")
nodes = pd.read_csv(collabs_graph_nodes_path)
nodes = hv.Dataset(nodes, "index")

# currently the most basic of chord diagrams with code from holoview tutorial
# TODO: fix visualisation
# in particular, is there a way to have the self-linking edges all be together?
# also, maybe restrict to value > a certain number, else it just looks like a yarn ball
chord = hv.Chord((edges, nodes))
chord.opts(
    opts.Chord(
        cmap="Category20",
        edge_cmap="Category20",
        edge_color=dim("source").str(),
        labels="nationality",
        node_color=dim("index").str(),
    )
)

# show(hv.render(chord))
# collabs_plot_path = os.path.join(CURR_FILEPATH, "collabs_plot.html")

# hv.save(chord, collabs_plot_path)
# hv.save(chord, collabs_plot_path)
