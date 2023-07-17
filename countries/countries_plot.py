import pandas as pd
import plotly.express as px

df = pd.read_csv("countries/CountryCount.csv").rename(columns={"count": "Count"})

countries_fig = px.choropleth(
    df,
    locations="iso3_codes",
    locationmode="ISO-3",
    hover_data={"Count": True, "iso3_codes": False},
    hover_name="country",
    color="Count",
    color_continuous_scale=px.colors.sequential.Purpor,
)

countries_fig.update_layout(
    autosize=False, margin=dict(l=0, r=0, b=0, t=0, pad=2, autoexpand=True), height=400
)

new_df = df[df["iso3_codes"].isin(["CAN", "RUS", "BRA", "AUS", "CHN"])]

countries_fig.add_scattergeo(
    locationmode="ISO-3",
    locations=new_df["iso3_codes"],
    text=new_df["Count"],
    mode="text",
    hoverinfo="skip",
    textfont=dict(color="black"),
    showlegend=False
)
usa = df[df["iso3_codes"] == "USA"]
countries_fig.add_scattergeo(
    locationmode="ISO-3",
    locations=usa["iso3_codes"],
    text=usa["Count"],
    mode="text",
    hoverinfo="skip",
    textfont=dict(color="white"),
    showlegend=False
)
fra_deu = df[df["iso3_codes"].isin(["FRA", "DEU"])]
countries_fig.add_scattergeo(
    locationmode="ISO-3",
    locations=fra_deu["iso3_codes"],
    text=fra_deu["Count"],
    mode="text",
    hoverinfo="skip",
    textfont=dict(size=7.5, color="red"),
    showlegend=False,
)
