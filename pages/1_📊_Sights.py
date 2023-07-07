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
with st.expander("Methodology"):
    st.markdown(
        """
        1. Each image is loaded using an image dataloader and custom dataset class for memory-efficient loading, with the help of PyTorch.
            - Each image is processed and resized to size 3 x 224 x 224.
            - Greyscale Images are converted to RGB format. 
        <details><summary>Show Code</summary>

        ```python
        from torch.utils.data import Dataset
        class CustomImageFolder(Dataset):
            TF = transforms.Compose(
                [transforms.Resize(
                    (224, 224), antialias=True), transforms.ToTensor()]
            )
            def __init__(self, img_dir, csv_dir, transform=TF):
                # ...
                self.transform = transform

            def __getitem__(self, idx):
                try:
                    img_link = self.data[idx]
                    img_id = int(img_link.split(".")[0]) # Gets image ID, for example 100346
                    img = (read_image(self.img_dir + "/" + img_link, ImageReadMode.RGB))
                # ...
        ```
        </details>

        2. ResNet152, a deep neural network used in image recognition is loaded, and its final fully-connected layer is removed.
        <details><summary>Show Code</summary>

        ```python
        import pytorch
        from torchvision import models
        model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT)
        # Remove final layer
        newmodel = torch.nn.Sequential(
            OrderedDict([*(list(model.named_children())[:-1])])
        )
        ```
        </details>

        3. Images are loaded as a tensor into ResNet152 in batches of 64 and fed through the model. The output of each image is a vector of length 2048.
        <details><summary>Show Code</summary>

        ```python
        datapoints = []
        list_labels = []
        with torch.no_grad():
        # ...
        newmodel.to("cuda") # Using GPU
        for i, (features, labels) in enumerate(dataloader): 
            # dataloader is a pytorch dataloader object.
            features = features.to("cuda") 
            # features is a batch of 64 images as (3 x 224 x 224) tensors
            outputs = np.squeeze(
                newmodel(features).to("cpu").numpy())
                .tolist() # A vector
            datapoints.extend(outputs)
            list_labels.extend(labels)
        ```
        </details>

        4. The resulting vectors are condensed into 3 dimensions using sklearn's t-SNE and plotted using Plotly's 3D scatterplot.
            - This plot is saved as a json file.

        <details><summary>Show Code</summary>

        ```python
        from sklearn.manifold import TSNE
        tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=400)
        X = tsne.fit_transform(X_prior)
        fig = px.scatter_3d(...)
        fig.write_json(...)
        ```
        </details>

        > More details can be found on Github.
    """,
    unsafe_allow_html=True)
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


