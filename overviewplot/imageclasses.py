import pandas as pd
import os
import re
import numpy as np

from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.io import read_image, ImageReadMode
from PIL import Image

class CustomImageFolder(Dataset):
    OPTIMAL_SIZE = [224, 224]
    TF = transforms.Compose(
        [transforms.Resize(OPTIMAL_SIZE, antialias=True),
        transforms.ToTensor()])
    def __init__(self, img_dir, csv_dir, transform=TF):
        df = pd.read_csv(csv_dir)
        self.csv = df[~df["Classification"].isnull()]
        self.img_dir = img_dir
        self.transform = transform
        self.data = [file for file in os.listdir(self.img_dir) if bool(re.search(r"\.(jp[e]?g|png)$", file)) and self.csv[self.csv["ObjectID"]== int(file.split(".")[0])]["Classification"].size == 1] # if the image has a class in the csv file.
        # fnmatch.filter(os.listdir(self.img_dir), '*.[jp][pn]g') does not support regex

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        try:
            img_link = self.data[idx]
            img_id = int(img_link.split(".")[0])
            img = (read_image(self.img_dir + "/" + img_link, ImageReadMode.RGB))
            img = transforms.ToPILImage()(img)
            if self.transform:
                img = self.transform(img)
            
            label = np.array(self.csv[self.csv["ObjectID"]==img_id]["Classification"])[0]
            return img, label 
        except Exception as e:
            raise Exception(f"Problem with image {img_id}. Exception: {e}")
    


    
