import os

import plotly.io


def read_from_json(string=os.path.abspath("./overview/overview_plot.json")):
    return plotly.io.read_json(string)


overview_plot = read_from_json()
