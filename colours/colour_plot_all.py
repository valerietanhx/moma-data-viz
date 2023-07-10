import pandas as pd
import plotly.express as px


def get_frequencies_of_basic_colour_groups():
    basic_palettes = pd.read_csv("colours/BasicPalettes.csv")
    basic_colour_groups = basic_palettes["BasicPalette"].values.tolist()
    combined = [colour for group in basic_colour_groups for colour in eval(group)]
    unique_colours = set(combined)
    frequencies = {colour: combined.count(colour) for colour in unique_colours}
    return frequencies


frequencies = get_frequencies_of_basic_colour_groups()
df = pd.DataFrame.from_dict(frequencies, orient="index")
df.reset_index(inplace=True)
df.columns = ["Colour", "Frequency"]
df["Colour"] = df["Colour"].str.capitalize()

# https://coolors.co/e2e2df-babab5-d0b19f-f0ba93-f6dea2-a0cfc5-9cc7e7-bba1e3-e89bc7-f39197
colours = {
    "Red": "#F39097",
    "Orange": "#F0BA93",
    "Yellow": "#F6DEA2",
    "Green": "#A0CFC5",
    "Blue": "#9CC6E7",
    "Purple": "#BBA1E3",
    "Pink": "#E89BC6",
    "Brown": "#D0B19F",
    "Grey": "#BABAB5",
    "White": "#E2E2DF",
}

fig = px.bar(
    df,
    x="Colour",
    y="Frequency",
    color="Colour",
    color_discrete_map=colours,
    hover_data=["Frequency"],
    title="Colours in MoMa artworks",
    text_auto="000",
)
fig.update_layout(xaxis={"categoryorder": "total descending"})
fig.update_layout(showlegend=False)
