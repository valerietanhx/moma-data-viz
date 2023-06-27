import streamlit as st
import streamlit.components.v1 as components

from colour_plot import fig_all as colour_fig_all
from colour_plot import fig_department as colour_fig_department

st.set_page_config(
    page_title="The Sights and Spaces of MoMa",
    page_icon="🎨",
)

st.title("The Sights and Spaces of MoMa")

st.header("Sights")

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
        - Plotly was used to generate the charts above based on the frequency
        of each of the basic colour names across the images.
        """
    )

st.write(
    """
    Most of the 83349 artworks (82301 of them, in fact—that's around 98.7%!) 
    have grey as a dominant colour. Here are some of the ones that don't.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/207.jpg")
    st.caption(
        "_Arch Oboler Guest House (Eleanor's Retreat), project,"
        + " Malibu, California, Perspective_ by Frank Lloyd Wight"
    )

with col2:
    st.image("images/8168.jpg")
    st.caption("_Otis Rush_ by Victor Moscoso, Raoul Ubac")

with col3:
    st.image("images/32764.jpg")
    st.caption("_Untitled from Moonstrips Empire News_ by Eduardo Paolozzi")

col4, col5, col6 = st.columns(3)

with col4:
    st.image("images/119718.jpg")
    st.caption("_Lips_ by Louise Bourgeois")

with col5:
    st.image("images/431484.jpg")
    st.caption("_You're an Indian?_ by Kay WalkingStick")

with col6:
    st.image("images/432544.jpg")
    st.caption("_Kusama_ by James Welling")

st.divider()

st.header("Spaces")

file = open("collabs_plot.html", "r", encoding="utf-8")
html = file.read()
components.html(html, width=800, height=800, scrolling=True)
