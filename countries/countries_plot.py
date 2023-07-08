import os

import pandas as pd
import plotly.express as px

df = pd.read_csv("countries/CountryCount.csv")

countries_fig = px.choropleth(
    df, 
    locations="iso3_codes", 
    locationmode="ISO-3", 
    hover_data={"count": True, "iso3_codes": False}, 
    hover_name="country",
    color="count",
    color_continuous_scale=px.colors.sequential.Purpor, 
)


