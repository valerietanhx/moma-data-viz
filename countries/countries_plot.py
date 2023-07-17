import pandas as pd
import plotly.express as px

df = pd.read_csv("countries/CountryCount.csv").rename(columns={"count": "Count"})

without_usa = df[df["iso3_codes"] != "USA" ]
countries_fig = px.choropleth(
    without_usa,
    locations="iso3_codes",
    locationmode="ISO-3",
    hover_data={"Count": True, "iso3_codes": False},
    hover_name="country",
    color="Count",
    color_continuous_scale=px.colors.sequential.Agsunset[::-1],
)

countries_fig.update_layout(
    autosize=False, margin=dict(l=0, r=0, b=0, t=0, pad=2, autoexpand=True), height=405
)
usa = df[df["iso3_codes"] == "USA"]

countries_fig.add_choropleth(
    False,
    locations = usa["iso3_codes"],
    locationmode="ISO-3",
    z=usa["Count"],
    showlegend=False,
    colorscale=["#29005e", "#29005e"],
    showscale= False,
    hovertemplate="""<b>USA</b><br><br>Count=%{z}<extra></extra>"""
)

countries_fig.add_scattergeo(
    locationmode="ISO-3",
    locations=usa["iso3_codes"],
    text=usa["Count"],
    mode="text",
    hoverinfo="skip",
    textfont=dict(color="white"),
    showlegend=False
)
