#%%
"This code converts nifti to pngs"


from PIL import Image
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from tqdm import tqdm
from matplotlib import pyplot as plt
from glob import glob
from pathlib import Path
imdirs = ['/mnt/bulk-neptune/marta/3Dclip/LUNG1/NifTi']
    #'/mnt/bulk-zen/marta/ct-data/ULS_data/ULS23/novel_data/ULS23_Radboudumc_Bone', 
#                     '/mnt/bulk-zen/marta/ct-data/ULS_data/ULS23/novel_data/ULS23_Radboudumc_Pancreas',
#                     '/mnt/bulk-zen/marta/ct-data/ULS_data/ULS23/processed_data/fully_annotated/kits21',
#                     '/mnt/bulk-zen/marta/ct-data/ULS_data/ULS23/processed_data/fully_annotated/LiTS',
#                     '/mnt/bulk-zen/marta/ct-data/ULS_data/ULS23/processed_data/fully_annotated/LIDC-IDRI']

outdir = Path('/mnt/bulk-neptune/marta/3Dclip/LUNG1/png_images/')
if not os.path.exists(outdir): os.mkdir(outdir)
imdir = []
# for path in imdirs:
#     imgs = glob(f'{path}/*.nii')
#     imdir.extend(imgs)

imdir = []
for root_dir in imdirs:
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.nii'):
                if not 'Eq_1' in file:
                    imdir.append(os.path.join(root, file))
#%%

files_per = np.random.permutation(imdir)
for file_name in tqdm(files_per):
    try:
        #if file_name == 'meta.csv' or file_name == 's0006' : continue
        file_name = Path(file_name)
        new_path = file_name.parts
        pt = new_path[-2]
        #tp = new_path[-2]
        imfile = new_path[-1].replace('.nii','')
        #imfile = new_path[-2]
        #odir: Path = outdir/Path(*new_path[6:-1])/imfile
        odir: Path = outdir/pt/imfile
        if not (odir/"done").exists():
            #nii_img  = nib.load(f'{imdir}/{file_name}/ct.nii.gz')
            nii_img  = nib.load(file_name)
            nii_data = nii_img.get_fdata()
            if len(nii_data.shape) == 4: nii_data = nii_data.squeeze()
            #hu_min, hu_max =  -1500, 500	#this should be an input variable
            window_levels = {'abdomen':['-175', '275'], 'chest':['-1500', '500']}
            for idx, window_level in enumerate(window_levels.values()):
            #window_level = windows.split(',')
                hu_min = float(window_level[0])
                hu_max = float(window_level[1])
                img_data = np.clip(nii_data, hu_min, hu_max)
                img_data = np.flip(np.flip(np.rot90(img_data),2),1)
                rescaled_image = (img_data-np.min(img_data))/(img_data.max()-np.min(img_data))*255 # float pixels
                image_array = np.uint8(rescaled_image) # integers pixels
                
                if odir.exists() and len(os.listdir(str(odir))) == image_array.shape[-1]:
                    continue 
                else:
                    if not odir.exists(): odir.mkdir(parents=True, exist_ok=True)
                    for id in range(image_array.shape[-1]):
                        final_image = Image.fromarray(image_array[:,:,id])
                        windowlabel = list(window_levels.keys())[idx]
                        final_image.save(f'{odir}/{imfile}_{windowlabel}_{id}.png')
                        #final_image.save(f'{odir}/{imfile}_{id}.png')
                    with open(f"{odir}/done","a") as f:
                        pass
    except Exception as exc:
        print(f'error{exc} with file {file_name}')

        
            
# saving the final output  
# as a PNG file 

# %%
