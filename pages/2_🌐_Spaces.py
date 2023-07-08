import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from collabs.collabs_cdf_plot import fig_cdf as collabs_fig_cdf

st.set_page_config(
    page_title="Spaces | The Sights and Spaces of MoMa",
    page_icon="🌐",
)

st.title("Spaces 🌐")

# choropleth plot to be inserted here
st.warning("Choropleth map to be inserted here!")

st.warning(
    """
    Choropleth map comments to be inserted here!
    """
)

st.markdown(
    """
    MoMa also presents art that transcends geographical boundaries,
    formed from international collaborations.
    """
)

file = open("collabs/collabs_chord_plot.html", "r", encoding="utf-8")
html = file.read()
components.html(html, width=800, height=600, scrolling=True)

with st.expander("Methodology"):
    st.markdown(
        """
        1. We kept the artworks attributed to at least two artists from different
        nationalities (i.e. intra-national collaborations were excluded).
        2. A collaboration between two nationalities refers to an artwork where at least
        one artist of each nationality contributed to the artwork.
        This means that an artwork by artists A1, A2, and B1, where artists A1 and A2
        are from country A and artist B1 is from country B, only counts as one
        collaboration between countries A and B, not two.
        3. HoloViews was used to create the chord diagram above.
        4. Only collaborations between two nationalities that occurred at least 20 times
        were plotted to strike a balance between engagement and clarity.
        """
    )

st.markdown(
    """
    Only 46 out of 481 collaborations between nationalities—just under 10%—occurred >=20
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
        1. We calculated the percentile of each unique frequency value x in descending
        order. This would correspond to the percentage of collaborations that occurred
        at least x times.
        2. Plotly was used to plot the line graph above.
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
