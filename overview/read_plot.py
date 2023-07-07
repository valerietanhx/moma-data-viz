import plotly.express as px
import plotly.io
import os 
#CURR_FILEPATH = os.path.dirname(__file__)
def read_from_json(string="overviewplot.json"):
    #return plotly.io.read_json(os.path.join(CURR_FILEPATH, string))
    return plotly.io.read_json(os.path.abspath("./overview/overviewplot.json"))

overview_plot = read_from_json()

