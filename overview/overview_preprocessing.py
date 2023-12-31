import gc
import logging
import random
from collections import OrderedDict

import numpy as np
import pandas as pd
import plotly.express as px
import torch
from image_classes import CustomImageFolder
from sklearn.manifold import TSNE
from torch.utils.data import DataLoader
from torchvision import models


def run():
    logging.debug(torch.cuda.is_available())
    BATCH_SIZE = 64

    model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT)
    newmodel = torch.nn.Sequential(OrderedDict([*(list(model.named_children())[:-1])]))
    # Remove fully connected layer and set the model to eval mode.
    newmodel.eval()

    dataset = CustomImageFolder("./colours/images/", "./Artworks.csv")
    dataloader = DataLoader(
        dataset, batch_size=BATCH_SIZE, shuffle=False
    )  # Preserve order

    # links to images
    id_images = [
        f"https://www.moma.org/collection/works/{filepath.split('.')[0]}"
        for filepath in dataset.data
    ]
    # This shows an image:
    # features, labels = next(iter(dataloader))
    # img = features[0]
    # plt.imshow(np.moveaxis(img.cpu().detach().numpy(), 0, -1) )
    # plt.show()

    datapoints = []
    list_labels = []
    with torch.no_grad():
        newmodel.to("cuda")
        for i, (features, labels) in enumerate(dataloader):
            features = features.to("cuda")
            outputs = np.squeeze(newmodel(features).to("cpu").numpy()).tolist()

            datapoints.extend(outputs)
            list_labels.extend(labels)
            logging.debug(f"Batch {i+1} Done")
            print(f"Batch {i+1} Done")

    CONSTANTNUM = 1000
    df = dataset.csv
    class_frequencies = list(
        map(
            lambda x: df[df["Classification"] == x].shape[0],
            df["Classification"].unique(),
        )
    )
    weighted_sampling_probability = CONSTANTNUM / np.array(class_frequencies)
    weighted_class_sampling_probabilities = {
        df["Classification"].unique()[i]: weighted_sampling_probability[i]
        for i in range(len(weighted_sampling_probability))
    }

    # use these probabilities to sample datapoints,
    # else we will have skewed distribution

    assert len(datapoints) == len(list_labels)

    sampled = [
        (datapoints[i], list_labels[i], id_images[i])
        for i in range(len(datapoints))
        if random.random() <= weighted_class_sampling_probabilities[list_labels[i]]
        and list_labels[i] != "(not assigned)"
    ]  # Remove unassigned labels
    assert len(sampled) > 0
    sampled_X, sampled_y, sampled_id = list(zip(*sampled))
    X_prior, y, id_arr = np.array(sampled_X), np.array(sampled_y), np.array(sampled_id)

    # TSNE for dimensionality reduction
    tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=400)
    X = tsne.fit_transform(X_prior)

    # Create dataframe
    dataframe = pd.DataFrame(X, columns=["x1", "x2", "x3"])
    dataframe["Classification"] = y
    dataframe["id"] = id_arr
    fig = px.scatter_3d(
        dataframe,
        x="x1",
        y="x2",
        z="x3",
        color="Classification",
        custom_data=["id"],
        width=900,
        height=800,
        text=dataframe["Classification"],
    )
    fig.update_traces(
        hovertemplate="<b>%{text}</b><br>MoMa link:<br>%{customdata}<br>(%{x}, %{y}, %{z})<extra></extra>",
        marker=dict(size=4),
        mode="markers",  # Hides text
    )
    fig.write_json("./overview/overview_plot.json")
    del model, newmodel
    clear_memory()


def clear_memory():
    torch.cuda.empty_cache()
    gc.collect()


run()
