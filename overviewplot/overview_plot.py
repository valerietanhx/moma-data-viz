import torch
import gc
import numpy as np
from imageclasses import CustomImageFolder
import matplotlib.pyplot as plt
from torchvision import models, datasets
from collections import OrderedDict
from torch.utils.data import DataLoader




model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT)
newmodel = torch.nn.Sequential(OrderedDict([*(list(model.named_children())[:-1])]))
# Remove fully connected layer
newmodel.eval()

dataset = CustomImageFolder('./colours/images/', './Artworks.csv')
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

#features, labels = next(iter(dataloader))
#img = features[0]
#plt.imshow(np.moveaxis(img.cpu().detach().numpy(), 0, -1) )
#plt.show()
with torch.no_grad():
    
    newmodel.to("cuda")
    for i, (features, labels) in enumerate(dataloader):
        features = features.to("cuda")
        print("hi")

torch.cuda.empty_cache()
gc.collect()

