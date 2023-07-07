import torch
import logging
import gc
import numpy as np
import pandas as pd
import plotly.express as px
import random
import time
from imageclasses import CustomImageFolder
from sklearn.manifold import TSNE
from torchvision import models, datasets
from collections import OrderedDict
from torch.utils.data import DataLoader

def run():
    
    logging.debug(torch.cuda.is_available())
    BATCH_SIZE = 64

    model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT)
    newmodel = torch.nn.Sequential(OrderedDict([*(list(model.named_children())[:-1])]))
    # Remove fully connected layer and set the model to eval mode.
    newmodel.eval()

    dataset = CustomImageFolder('./colours/images/', './Artworks.csv')
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False) # Preserve order
    
    # links to images
    id_images = [f"https://www.moma.org/collection/works/{filepath.split('.')[0]}" for filepath in dataset.data]
    assert(len(id_images)==83341) 
    # This shows an image:
    # features, labels = next(iter(dataloader))
    # img = features[0]
    # plt.imshow(np.moveaxis(img.cpu().detach().numpy(), 0, -1) )
    # plt.show()

    FEATURES = 2048
    datapoints = []
    list_labels = []
    with torch.no_grad():
        points = "empty"  
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
    class_frequencies = list(map(lambda x: df[df["Classification"] == x].shape[0], df["Classification"].unique()))
    weighted_sampling_probability = CONSTANTNUM / np.array(class_frequencies) 
    weighted_class_sampling_probabilities = {df["Classification"].unique()[i] : weighted_sampling_probability[i] for i in range(len(weighted_sampling_probability))}

    # use these probabilities to sample datapoints, 
    # else we will have skewed distribution

    assert(len(datapoints) == len(list_labels))

    sampled = [(datapoints[i], list_labels[i], id_images[i]) for i in range(len(datapoints)) if random.random() <= weighted_class_sampling_probabilities[list_labels[i]]]
    assert(len(sampled)>0)
    sampled_X, sampled_y, sampled_id = list(zip(*sampled))
    X_prior, y, id_arr = np.array(sampled_X), np.array(sampled_y), np.array(sampled_id)

    # TSNE for dimensionality reduction
    tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=400)
    X = tsne.fit_transform(X_prior)

    # Create dataframe
    dataframe = pd.DataFrame(X, columns = ['x1', 'x2', 'x3'])
    dataframe['class'] = y
    dataframe['id'] = id_arr
    fig = px.scatter_3d(dataframe, x="x1", y="x2", z="x3", color='class', custom_data=['id'])
    fig.update_traces(hovertemplate='<b>Moma</b>:<br>%{customdata}<br>(%{x}, %{y}, %{z})')
    
    fig.write_json("./overviewplot/overviewplot.json")
    clear_memory()
    

def clear_memory():
    torch.cuda.empty_cache()
    gc.collect()

run()