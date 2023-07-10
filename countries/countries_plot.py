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

countries_fig.update_layout(
    autosize=False, margin=dict(l=0, r=0, b=0, t=0, pad=2, autoexpand=True), height=500
)
