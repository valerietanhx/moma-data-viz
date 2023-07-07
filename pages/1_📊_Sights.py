import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from collabs.collabs_cdf_plot import fig_cdf as collabs_fig_cdf
from colours.colour_plot import fig_all as colour_fig_all
from colours.colour_plot import fig_department as colour_fig_department
from overview.read_plot import overview_plot

st.set_page_config(
    page_title="The Sights of MoMa",
    page_icon="🎨",
)

st.title("Sights")

st.subheader("Overview")

st.markdown(
    """We begin this theme with an overview of the art collection, revealing patterns in the artwork’s formal qualities that might not be immediately apparent.
    A proportion of art pieces are shown on the scatterplot below, capturing how similar or dissimilar pieces are to one another.
"""
)
st.plotly_chart(overview_plot, theme=None)

st.subheader("Colours")
st.divider()
st.write("Let's explore the colours of the artworks in MoMa's art collection.")

tab1, tab2 = st.tabs(["All artworks", "By department"])
with tab1:
    st.plotly_chart(colour_fig_all)
with tab2:
    st.plotly_chart(colour_fig_department)

with st.expander("Methodology"):
    st.markdown(
        """
        - [aiohttp](https://docs.aiohttp.org/en/stable/) was used to download all
        thumbnail images available.
        - For each image, we retrieved an RGB colour palette of the six most dominant
        colours in it with the [ColorThief](https://github.com/fengsp/color-thief-py)
        module, before converting each hex code to the name of the closest named CSS
        colour with the [webcolors](https://pypi.org/project/webcolors/) module.
        - We then mapped each CSS colour name to one of ten basic colour names:
        red, orange, yellow, green, blue, purple, pink, brown, grey, and white.
        The mapping was inspired by
        [w3school](https://www.w3schools.com/colors/colors_groups.asp) and
        [Austin Gil](https://austingil.com/css-named-colors/)'s mappings,
        but modified slightly by us based on our own perception of the colours.
        - Plotly was used to create the charts above based on the frequency
        of each of the basic colour names across the images.
        """
    )

st.write(
    """
    Most of the 83349 artworks (82301 of them, in fact—that's around 98.7%!) 
    have grey as one of their dominant colours. Here are some that don't!
    """
)

artworks_without_grey = pd.read_csv("colours/ArtworksWithoutGrey.csv")
random_six = artworks_without_grey.sample(6)


def show_random_image_without_grey(idx):
    row = random_six.iloc[idx]
    object_id = int(row["ObjectID"])
    title = row["Title"]
    artists = row["Artist"]
    st.image(f"colours/images/{object_id}.jpg")
    st.caption(f"_{title}_ by {artists}")


col1, col2, col3 = st.columns(3)

with col1:
    show_random_image_without_grey(0)

with col2:
    show_random_image_without_grey(1)

with col3:
    show_random_image_without_grey(2)

col4, col5, col6 = st.columns(3)

with col4:
    show_random_image_without_grey(3)

with col5:
    show_random_image_without_grey(4)

with col6:
    show_random_image_without_grey(5)

st.write(
    """
    (Some of these artworks may still look like they have black or grey in them.
    Our colour detection method isn't quite perfect yet, it seems :"))
    """
)

st.divider()
####################################################################################################################################


