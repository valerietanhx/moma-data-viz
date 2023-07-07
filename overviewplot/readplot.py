import plotly.express as px
import plotly.io



def read_from_json(string="./overviewplot/overviewplot.json"):
    return plotly.io.read_json(string)

overview_plot = read_from_json()

