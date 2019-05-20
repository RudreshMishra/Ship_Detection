from torch.utils.data import DataLoader
from torchvision import transforms
from pathlib import Path
import csv
from PIL import Image
import numpy as np

def get_dl(training: bool,batch_size:int, **kwargs):
	dataset = Ships_Datasets(training = training)
	return DataLoader(dataset,batch_size = batch_size, **kwargs)

normalize = transforms.Normalize(mean = [0.485,0.456,0.406],
                                std = [0.229,0.224,0.225])


class Ships_Datasets:
    def __init__(self,training: bool):
        self.path =Path('/media/rudresh/New Volume 1/Air_bus/jupyter_notebook')
        mask_data_frame = self.path/'train_ship_segmentations_v2.csv'
        self.image_fnames = []        
        self.rows = []
        with open(str(mask_data_frame)) as f:
            segmentation_csv =  csv.reader(f)
            for row in segmentation_csv:
                self.rows.append(row)
                self.image_fnames.append(self.path/'train_v2'/row[0])
                
        del self.rows[0]
        del self.image_fnames[0]
            
        self.transforms = transforms.Compose([
                transforms.ToTensor(),
                normalize,
        ])
    def __len__(self):
        return len(self.rows)
    
    def __getitem__(self,idx):
        rgb = Image.open(str(self.image_fnames[idx]))
        mask = np.zeros(rgb.size[0]*rgb.size[1])
        for pixel, runlen in pairwise(self.rows[idx][-1].split()):
            print(pixel,runlen)
            mask[int(pixel):int(pixel)+int(runlen)] = 1
        mask_img = mask.reshape((768,768))
        flipped_mask = np.flipud(np.rot90(mask_img))
        
        normalized_rgb = self.transforms(rgb)
        
        return{
            'gt':flipped_mask,
            'normalized_rgb':normalized_rgb,}
        
        
def pairwise(it):
    it = iter(it)
    while True:
        try:
            yield next(it),next(it)
        except StopIteration:
            return
        
        
            
        
