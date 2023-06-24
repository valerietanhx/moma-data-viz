import holoviews as hv
import pandas as pd

# from bokeh.plotting import show
from holoviews import dim, opts

hv.extension("bokeh")
hv.output(size=200)

edges = pd.read_csv("CollabsGraphEdges.csv")
nodes = pd.read_csv("CollabsGraphNodes.csv")
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
# hv.save(chord, "collabs_plot.html")
