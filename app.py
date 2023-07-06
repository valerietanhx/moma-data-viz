import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from collabs.collabs_cdf_plot import fig_cdf as collabs_fig_cdf
from colours.colour_plot import fig_all as colour_fig_all
from colours.colour_plot import fig_department as colour_fig_department

st.set_page_config(
    page_title="The Sights and Spaces of MoMa",
    page_icon="🎨",
)

st.title("The Sights and Spaces of MoMa")

st.header("Sights")

st.subheader("Colours")

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

st.header("Spaces")

st.subheader("International collaborations")

st.write("What international collaborations are there in MoMa's art collection?")

file = open("collabs/collabs_plot.html", "r", encoding="utf-8")
html = file.read()
components.html(html, width=800, height=600, scrolling=True)

with st.expander("Methodology"):
    st.markdown(
        """
        - We kept the artworks attributed to at least two artists from different
        nationalities (i.e. intra-national collaborations were excluded).
        - A collaboration between two nationalities refers to an artwork where at least
        one artist of each nationality contributed to the artwork.
        This means that an artwork by artists A1, A2, and B1, where artists A1 and A2
        are from country A and artist B1 is from country B, only counts as one
        collaboration between countries A and B, not two.
        - HoloViews was used to create the chord diagram above.
        - Only collaborations between two nationalities that occurred at least 18 times
        were plotted to strike a balance between engagement and clarity.
        """
    )

st.write(
    """
    Only 49 out of 481 collaborations between nationalities—just over 10%—occurred >=18
    times! While many international collaborations appear in MoMa's collection,
    most of them seem to have been short-lived partnerships.
    
    (Though we are, of course, merely looking at nationalities and not individuals;
    we cannot conclude that this observation reflects nations' bilateral ties.)
    """
)

st.plotly_chart(collabs_fig_cdf)

with st.expander("Methodology"):
    st.markdown(  # might be unclear, to rework
        """
        - We calculated the percentile of each unique frequency value x in descending
        order. This would correspond to the percentage of collaborations that occurred
        at least x times.
        - Plotly was used to plot the line graph above.
        """
    )

st.write(
    """
    Want a more granular view? Pick two nationalities and discover
    art born from the collaboration of their artists!
    """
)

nodes = pd.read_csv("collabs/CollabsGraphNodes.csv")
nationalities = nodes["nationality"]

# pick first nationality
first_nationality = st.selectbox("First nationality", nationalities)

# get nationalities that selected nationality has collaborated with
first_nationality_index = nodes.query(f"`nationality` == '{first_nationality}'")[
    "index"
].tolist()[0]
edges_selection = pd.read_csv("collabs/CollabsSelectionEdges.csv")
collab_nationalities = edges_selection.query(f"`source` == {first_nationality_index}")
collab_nationalities = collab_nationalities.merge(
    nodes, how="left", left_on="target", right_on="index"
)

# pick second nationality out of the filtered nationalities
second_nationality = st.selectbox(
    "Second nationality", collab_nationalities["nationality"]
)

# find matches
collabs = pd.read_csv("collabs/Collabs.csv")
matches = collabs.query(
    f"`Nationality`.str.contains('{first_nationality}') &"
    + f"`Nationality`.str.contains('{second_nationality}')"
)

# don't think this should appear given the way streamlit options work?
# but leaving here for now in case
if len(matches) == 0:
    st.info(
        f"""
        Sorry, we don't know of any collaborations between
        {first_nationality} and {second_nationality} artists :(
        """
    )
else:
    matches_with_thumbnails = matches.dropna(subset=["ThumbnailURL"])
    if len(matches_with_thumbnails) == 0:
        st.write(
            f"""
            {first_nationality} and {second_nationality} artists have collaborated
            {len(matches)} time(s), but we don't have images for their works!
            Here are some of their artwork titles instead:
            """
        )
        filtered = matches.filter(["Title", "Artist", "Nationality"], axis=1)
        filtered = filtered.rename(
            {"Artist": "Artists", "Nationality": "Nationalities"}, axis=1
        )

        filtered["Nationalities"] = filtered["Nationalities"].apply(
            lambda row: ", ".join(
                nat if nat else "[Unknown]" for nat in re.findall(r"\((.*?)\)", row)
            )
        )

        # css to hide row indices of table
        hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
        # inject css with markdown
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # display dataframe
        if len(filtered) <= 5:
            st.table(filtered)
        else:
            st.table(filtered.sample(5))
    else:
        st.write(
            f"""
            {first_nationality} and {second_nationality} artists have collaborated
            {len(matches)} time(s)!
            Here's a random artwork born from one of their collaborations:
            """
        )
        random_artwork = matches_with_thumbnails.sample()
        object_id = int(random_artwork["ObjectID"].tolist()[0])
        title = random_artwork["Title"].tolist()[0]
        artists = random_artwork["Artist"].tolist()[0]
        with st.columns(3)[1]:
            st.image(f"colours/images/{object_id}.jpg")
            st.caption(f"_{title}_ by {artists}")
