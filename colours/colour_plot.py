import os

import pandas as pd
import plotly.express as px

CURR_FILEPATH = os.path.dirname(__file__)


def get_frequencies_of_basic_colour_groups():
    basic_palettes_path = os.path.join(CURR_FILEPATH, "BasicPalettes.csv")
    basic_palettes = pd.read_csv(basic_palettes_path)
    basic_colour_groups = basic_palettes["BasicPalette"].values.tolist()
    combined = [colour for group in basic_colour_groups for colour in eval(group)]
    unique_colours = set(combined)
    frequencies = {colour: combined.count(colour) for colour in unique_colours}
    return frequencies


frequencies_all = get_frequencies_of_basic_colour_groups()
df_all = pd.DataFrame.from_dict(frequencies_all, orient="index")
df_all.reset_index(inplace=True)
df_all.columns = ["Colour", "Frequency"]
df_all["Colour"] = df_all["Colour"].str.capitalize()

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

fig_all = px.bar(
    df_all,
    x="Colour",
    y="Frequency",
    color="Colour",
    color_discrete_map=colours,
    hover_data=["Frequency"],
    title="Colours in MoMa artworks",
    text_auto="000",
)  # tbh, the number labels defeat the purpose of interactivity? :/
fig_all.update_layout(xaxis={"categoryorder": "total descending"})
fig_all.update_layout(showlegend=False)


def get_frequencies_of_basic_colour_groups_by_department():
    basic_palettes_path = os.path.join(CURR_FILEPATH, "BasicPalettes.csv")
    basic_palettes = pd.read_csv(basic_palettes_path)
    thumbnails_path = os.path.join(CURR_FILEPATH, "ArtworksWithThumbnails.csv")
    artworks_with_thumbnails = pd.read_csv(thumbnails_path)
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


df_department = get_frequencies_of_basic_colour_groups_by_department()
df_department["Colour"] = df_department["Colour"].str.capitalize()

fig_department = px.histogram(
    df_department,
    x="Department",
    y="Frequency",
    color="Colour",
    barnorm="percent",
    title="Colours in MoMa artworks by department",
    color_discrete_map=colours,
)  # TODO: fix hover text + standardise order of colours
fig_department.update_layout(yaxis_title="Percentage")
fig_department.update_layout(showlegend=False)
fig_department.update_layout(yaxis_ticksuffix="%")
