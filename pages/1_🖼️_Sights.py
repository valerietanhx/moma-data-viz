import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sights | The Sights and Spaces of MoMa",
    page_icon="🖼️",
)

with st.sidebar:
    st.caption(
        "Source code on 🖥️ [GitHub](https://github.com/valerietanhx/moma-data-viz/)."
    )

with st.spinner("Loading..."):
    from colours.colour_plot_all import fig as colour_fig_all
    from colours.colour_plot_department import fig as colour_fig_department
    from overview.overview_plot import overview_plot

st.title("Sights 🖼️")

st.subheader("Overview")

st.markdown(
    """
    We begin this theme with an overview of the art collection, revealing patterns
    in the artworks' formal qualities that might not be immediately apparent.
    A random sample of artworks is shown on the scatterplot below, capturing how
    visually similar or dissimilar artworks are to one another.
    
    Hover around the graph to view details of each individual artwork, including
    the link to their individual page on the MoMa website.
    Double-click a category in the panel on the right to only view artworks that fall
    under that specific category, and double-click to unselect.
    """
)

with st.spinner("Loading..."):
    st.plotly_chart(overview_plot, theme=None)

with st.expander("Methodology"):
    st.markdown(
        """
        1. Each image was resized to 3px x 224px x 224px and loaded with PyTorch,
        using an image DataLoader and custom Dataset class for memory-efficient loading.
        2. We made use of ResNet152, a deep neural network used in image recognition.
        This model was loaded and its final fully-connected layer was removed.
        3. Images were fed into ResNet152 in batches of 64. The output of each image was
        a vector of length 2048.
        4. Because some classification types are more common than others, we took a
        smaller sample of more common artforms to achieve a more even distribution.
        5. The resulting vectors were condensed from 2048 to three dimensions using
        sklearn's t-SNE.
        6. Plotly was used to plot the 3D scatterplot above, which was then saved as
        a json file.

        More details can be found on
        🖥️ [GitHub](https://github.com/valerietanhx/moma-data-viz/tree/master/overview).
        """
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
        colour with the [webcolors](https://pypi.org/project/webcolors/) module and
        a KDTree data structure, which finds the closest colour in the rgb space
        based on Euclidean distance.
        3. We then mapped each CSS colour name to one of ten basic colour names:
        red, orange, yellow, green, blue, purple, pink, brown, grey, and white.
        The mapping was inspired by
        [w3school](https://www.w3schools.com/colors/colors_groups.asp) and
        [Austin Gil](https://austingil.com/css-named-colors/)'s mappings,
        but modified slightly by us based on our own perception of the colours.
        4. Plotly was used to create the bar charts above based on the frequency
        of each of the basic colour names across the images.

        More details can be found on
        🖥️ [GitHub](https://github.com/valerietanhx/moma-data-viz/tree/master/colours).
        """
    )

st.markdown(
    """
    Most of the 83349 artworks (82301 of them, in fact—that's around 98.7%!) 
    have grey as one of their six dominant colours, contrary to what we might expect of
    modern art. Here are some that don't!

    (Some of these artworks may still look like they have black or grey in them;
    our colour detection method sadly isn't perfect.)
    """
)

basic_palettes = pd.read_csv("colours/BasicPalettes.csv")
artworks_with_thumbnails = pd.read_csv("colours/ArtworksWithThumbnails.csv")
merged = basic_palettes.merge(artworks_with_thumbnails, on="ObjectID")


def show_random_image(sample, idx):
    row = sample.iloc[idx]
    url = row["ThumbnailURL"]
    title = row["Title"]
    artists = row["Artist"]
    st.image(url)
    st.caption(f"_{title}_ by {artists}")


artworks_without_grey = merged.query("~`BasicPalette`.str.contains('grey')")
random_six_without_grey = artworks_without_grey.sample(6)
random_six_without_grey["Artist"] = random_six_without_grey["Artist"].apply(
    lambda row: ", ".join(
        map(
            lambda x: "[Various Artists]" if x == "Various Artists" else x,
            row.split(", "),
        )
    )
)

col1, col2, col3 = st.columns(3)

with col1:
    show_random_image(random_six_without_grey, 0)

with col2:
    show_random_image(random_six_without_grey, 1)

with col3:
    show_random_image(random_six_without_grey, 2)

col4, col5, col6 = st.columns(3)

with col4:
    show_random_image(random_six_without_grey, 3)

with col5:
    show_random_image(random_six_without_grey, 4)

with col6:
    show_random_image(random_six_without_grey, 5)

st.markdown(
    """
    On the other end of the spectrum is orange, with only 67 artworks featuring it
    as one of their six dominant colours. (It's likely that more artworks actually
    feature orange, but featured a shade more similar to brown, and which was thus
    read as such.)
    
    Which artworks have orange in them?

    (Once again, some of these artworks may not appear to contain orange.
    One limitation of our method of mapping colours to names is that it often confuses
    orange and yellow colours :"))
    """
)

artworks_with_orange = merged.query("`BasicPalette`.str.contains('orange')")
random_six_with_orange = artworks_with_orange.sample(6)
random_six_with_orange["Artist"] = random_six_with_orange["Artist"].apply(
    lambda row: ", ".join(
        map(
            lambda x: "[Various Artists]" if x == "Various Artists" else x,
            row.split(", "),
        )
    )
)

col7, col8, col9 = st.columns(3)

with col7:
    show_random_image(random_six_with_orange, 0)

with col8:
    show_random_image(random_six_with_orange, 1)

with col9:
    show_random_image(random_six_with_orange, 2)

col10, col11, col12 = st.columns(3)

with col10:
    show_random_image(random_six_with_orange, 3)

with col11:
    show_random_image(random_six_with_orange, 4)

with col12:
    show_random_image(random_six_with_orange, 5)
