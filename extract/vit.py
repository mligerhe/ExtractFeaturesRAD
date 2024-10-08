#!/usr/bin/env python3
import torchvision
import torch
from fire import Fire
from extract_rad import extract_features_
from getcuda import get_free_gpu_indices

__all__ = ['extract_vit_imagenet_features_']


def extract_vit_imagenet_features_(*slide_tile_paths, **kwargs):
    """Extracts features from slide tiles.

    Args:
        slide_tile_paths:  A list of paths containing the slide tiles, one
            per slide.
        outdir:  Path to save the features to.
        augmented_repetitions:  How many additional iterations over the
            dataset with augmentation should be performed.  0 means that
            only one, non-augmentation iteration will be done.
    """
    model = torchvision.models.vit_b_16(weights = 'IMAGENET1K_V1')
    model.heads = torch.nn.Identity()
    #device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device_ids = get_free_gpu_indices()
    if len(device_ids)==0:
        device = 'cpu'
    else:
        device='cuda:'+str(device_ids[0])

    print(device)

    model = model.eval().to(device)

    return extract_features_(slide_tile_paths=slide_tile_paths, **kwargs, model=model, model_name='vit-imagenet')


if __name__ == '__main__':
    Fire(extract_vit_imagenet_features_)



