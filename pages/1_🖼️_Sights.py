import pandas as pd
import streamlit as st

from colours.colour_plot import fig_all as colour_fig_all
from colours.colour_plot import fig_department as colour_fig_department
from overview.overview_plot import overview_plot

st.set_page_config(
    page_title="Sights | The Sights and Spaces of MoMa",
    page_icon="🖼️",
)

st.title("Sights 🖼️")

st.subheader("Overview")

st.markdown(
    """We begin this theme with an overview of the art collection, revealing patterns
    in the artwork's formal qualities that might not be immediately apparent.
    A proportion of art pieces are shown on the scatterplot below, capturing how
    similar or dissimilar pieces are to one another.
    """
)

st.plotly_chart(overview_plot, theme=None)

with st.expander("Methodology"):
    st.markdown(
        """
        1. Each image is resized to size 3 x 224 x 224 and loaded with PyTorch,
        using an image DataLoader and custom Dataset class for memory-efficient loading.
        2. We make use of ResNet152, a deep neural network used in image recognition.
        This model is loaded and its final fully-connected layer is removed.
        3. Images are fed into ResNet152 in batches of 64. The output of each image is
        a vector of length 2048.
        4. Because some classification types are more common than others, we took a
        smaller sample of more common artforms to achieve a more even distribution.
        5. The resulting vectors were condensed from 2048 to three dimensions using
        sklearn's t-SNE.
        6. Plotly was used to plot the 3D scatterplot above, which was then saved as
        a json file.

        More details can be found on
        🖥️[Github](https://github.com/valerietanhx/moma-data-viz/tree/master/overview).
        """,
    )

st.markdown(
    """Now, we focus on one particular dimension of art: colour. Colour, as our
    first sense and the sense through which most people best navigate the world,
    holds immense significance in art and human experience. We aim to explore the
    colours that dominate MoMA's collection, revealing the palette of modern art.
    """
)

tab1, tab2 = st.tabs(["All artworks", "By department"])
with tab1:
    st.plotly_chart(colour_fig_all)
with tab2:
    st.plotly_chart(colour_fig_department)

with st.expander("Methodology"):
    st.markdown(
        """
        1. [aiohttp](https://docs.aiohttp.org/en/stable/) was used to download all
        thumbnail images available.
        2. For each image, we retrieved an RGB colour palette of the six most dominant
        colours in it with the [ColorThief](https://github.com/fengsp/color-thief-py)
        module, before converting each hex code to the name of the closest named CSS
        colour with the [webcolors](https://pypi.org/project/webcolors/) module.
        3. We then mapped each CSS colour name to one of ten basic colour names:
        red, orange, yellow, green, blue, purple, pink, brown, grey, and white.
        The mapping was inspired by
        [w3school](https://www.w3schools.com/colors/colors_groups.asp) and
        [Austin Gil](https://austingil.com/css-named-colors/)'s mappings,
        but modified slightly by us based on our own perception of the colours.
        4. Plotly was used to create the bar charts above based on the frequency
        of each of the basic colour names across the images.
        """
    )

st.markdown(
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

st.markdown(
    """
    (Some of these artworks may still look like they have black or grey in them.
    Our colour detection method isn't quite perfect yet, it seems :"))
    """
)
