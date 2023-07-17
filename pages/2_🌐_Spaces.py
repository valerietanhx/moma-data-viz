import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from collabs.collabs_cdf_plot import fig_cdf as collabs_fig_cdf
from countries.countries_plot import countries_fig

st.set_page_config(
    page_title="Spaces | The Sights and Spaces of MoMa",
    page_icon="🌐",
)

st.title("Spaces 🌐")

# css to hide row indices of table
hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
    """
# inject css with markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.plotly_chart(countries_fig, theme=None)

st.markdown(
    """
    The collection is overwhelmingly American with a total of 5191 artists from the
    United States, though this is to be expected of an American museum.
    
    Following far behind in second place is Germany with
    965 artists represented, then the United Kingdom, France, and Italy with
    860, 845, and 536 artists respectively. Notably, these are all countries in the
    Western world, while few African or Asian artists appear in MoMa's art collection,
    suggesting that the collection may not be fully representative of the global
    modern art landscape.

    What about the _least_ represented countries? Here are the artists solo-representing
    the countries they come from!
    """
)

solo_representations = pd.read_csv("countries/SoloRepresentationsEnhanced.csv")
solo_representations = solo_representations[["DisplayName", "Nationality", "URL"]]
solo_representations = solo_representations.rename(columns={"DisplayName": "Name"})

st.table(solo_representations)

st.markdown(
    """
    MoMa also presents art that transcends geographical boundaries,
    formed from international collaborations. We present here pairs of countries that
    have collaborated at least 20 times.

    Click on a country's chords to highlight it and get a clearer view of its
    international collaborations!
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

        More details can be found on
        🖥️ [Github](https://github.com/valerietanhx/moma-data-viz/tree/master/collabs).
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

        More details can be found on
        🖥️ [Github](https://github.com/valerietanhx/moma-data-viz/tree/master/collabs).
        """
    )

st.write(
    """
    Want a more granular view? Pick two nationalities and discover
    art born from the collaboration of their artists!
    """
)

edges_selection = pd.read_csv("collabs/CollabsSelectionEdges.csv")
nationalities = edges_selection["source"].unique()

# pick first nationality
first_nationality = st.selectbox("First nationality", nationalities)

# get nationalities that selected nationality has collaborated with
edges_selection = pd.read_csv("collabs/CollabsSelectionEdges.csv")
collab_nationalities = edges_selection.query(f"`source` == '{first_nationality}'")[
    "target"
].unique()

# pick second nationality out of the filtered nationalities
second_nationality = st.selectbox("Second nationality", collab_nationalities)

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
    num_collabs = len(matches)
    num_times = ""
    if num_collabs == 1:
        num_times = "once"
    elif num_collabs == 2:
        num_times = "twice"
    elif 3 <= num_collabs <= 9:
        NUMBERS_DICT = {
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
        }
        num_times = NUMBERS_DICT[num_collabs] + " times"
    else:
        num_times = str(num_collabs) + " times"

    matches_with_thumbnails = matches.dropna(subset=["ThumbnailURL"])
    if len(matches_with_thumbnails) == 0:
        st.write(
            f"""
            {first_nationality} and {second_nationality} artists have collaborated
            {num_times}, but we don't have images for their works!
            Here are some of their artwork titles instead:
            """
        )
        filtered = matches.filter(["Title", "Artist", "Nationality", "URL"], axis=1)
        filtered = filtered.rename(
            {"Artist": "Artists", "Nationality": "Nationalities"}, axis=1
        )

        filtered["Nationalities"] = filtered["Nationalities"].apply(
            lambda row: ", ".join(
                nat if nat else "[Unknown]" for nat in re.findall(r"\((.*?)\)", row)
            )
        )

        filtered["URL"] = filtered["URL"].fillna("[Not available]")

        # display dataframe
        if len(filtered) <= 5:
            st.table(filtered)
        else:
            st.table(filtered.sample(5))
    else:
        st.write(
            f"""
            {first_nationality} and {second_nationality} artists have collaborated
            {num_times}!
            Here's a random artwork born from one of their collaborations:
            """
        )
        random_artwork = matches_with_thumbnails.sample()
        title = random_artwork["Title"].tolist()[0]
        artists = random_artwork["Artist"].tolist()[0]
        with st.columns(3)[1]:
            url = random_artwork["ThumbnailURL"].tolist()[0]
            st.image(url)
            st.caption(f"_{title}_ by {artists}")
