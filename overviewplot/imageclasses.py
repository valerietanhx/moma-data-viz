import torch
import os
import fnmatch
import torchvision
from torch.utils.data import Dataset
from torchvision import transforms, models, datasets
from torchvision.io import read_image
from PIL import Image

class CustomImageFolder(Dataset):
    OPTIMAL_SIZE = (224, 224)
    def __init__(self, root_dir, transform=transforms.Compose(
            [transforms.Resize(OPTIMAL_SIZE, antialias=True), transforms.ToTensor()])):
        self.root_dir = root_dir
        self.transform = transform
        self.data = fnmatch.filter(os.listdir(self.root_dir), '*.[jp][pn]g')

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        #t = transforms.ToPILImage()
        img = (read_image(self.root_dir + "/" + self.data[idx]))
        
        img = transforms.ToPILImage()(img)
 
        if self.transform:
            img = self.transform(img)

        return img # No label
    
    
    


# a = CustomImageFolder("./colours/images/")
# print(len(a))

