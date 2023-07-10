import pandas as pd
import plotly.express as px


def get_frequencies_of_basic_colour_groups_by_department():
    basic_palettes = pd.read_csv("colours/BasicPalettes.csv")
    artworks_with_thumbnails = pd.read_csv("colours/ArtworksWithThumbnails.csv")
    merged = basic_palettes.merge(artworks_with_thumbnails, on="ObjectID")
    df_as_list = []
    for department in list(merged["Department"].unique()):
        art_in_department = merged.query(f"`Department` == '{department}'")
        basic_colour_groups = art_in_department["BasicPalette"].values.tolist()
        combined = [colour for group in basic_colour_groups for colour in eval(group)]
        unique_colours = set(combined)
        for colour in unique_colours:
            count = combined.count(colour)
            df_as_list.append((department, colour, count))
    return pd.DataFrame(df_as_list, columns=["Department", "Colour", "Frequency"])


df = get_frequencies_of_basic_colour_groups_by_department()
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

fig = px.histogram(
    df,
    x="Department",
    y="Frequency",
    color="Colour",
    barnorm="percent",
    title="Colours in MoMa artworks by department",
    color_discrete_map=colours,
)  # TODO: fix hover text + standardise order of colours
fig.update_layout(yaxis_title="Percentage")
fig.update_layout(showlegend=False)
fig.update_layout(yaxis_ticksuffix="%")
