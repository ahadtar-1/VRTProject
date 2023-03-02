"""
The module comprises of the different operations to be performed on videoframes
"""

import cv2
import glob
import os
import torch
import requests
import numpy as np
import shutil
from os import path as osp
from collections import OrderedDict
from torch.utils.data import DataLoader
from models.network_vrt import VRT as net
from utils import utils_image as util
from data.dataset_video_test import VideoRecurrentTestDataset, VideoTestVimeo90KDataset, SingleVideoRecurrentTestDataset, VFI_DAVIS, VFI_UCF101, VFI_Vid4
from main_test_vrt import prepare_model_dataset, test_video
from PIL import Image


def save_frames(filePath: str)-> None:
    """
    The function splits the video into image frames

    Parameters
    ----------
    str

    Returns
    -------
    None

    """

    cam = cv2.VideoCapture(filePath)    
    currentFrame = 1 
    while True:
        ret, frame = cam.read()
        if ret:
            name = 'frame0000000' + str(currentFrame) + ".png"
            cv2.imwrite(name, frame)
            inputFolder = 'testsets/uploaded/000'
            dst_path = os.path.join(inputFolder, name)
            print(f'move {name} to {dst_path}')
            shutil.move(name, dst_path)
            currentFrame += 1    	     	
        else:
    	    break
    	    
    cam.release()
    cv2.destroyAllWindows()


def video_superresolution(filePath: str)-> str:   
    """
    The function performs superresolution on a video
    
    Parameters
    ----------
    str
    
    Returns
    -------
    str
    
    """

    save_frames(filePath)
    #os.chdir('./')
    modelDict = {'folder_gt': None, 'folder_lq': 'testsets/uploaded', 'nonblind_denoising': False,
                 'num_workers': 2, 'save_result': True, 'scale': 4, 'sigma': 0,
                 'task': '001_VRT_videosr_bi_REDS_6frames', 'tile': [40,64,64], 'tile_overlap': [2,20,20],
                 'window_size': [6,8,8]}

    device = torch.device('cpu')
    model = prepare_model_dataset(modelDict)
    model.eval()
    model = model.to(device)
    test_set = SingleVideoRecurrentTestDataset({'dataroot_gt': None, 'dataroot_lq': modelDict.get('folder_lq'),
                                              'sigma': modelDict.get('sigma'), 'num_frame': -1, 'cache_data': False})
    test_loader = DataLoader(dataset = test_set, num_workers = modelDict.get('num_workers'), batch_size = 1, shuffle = False)
    #print(test_loader)
    save_dir = 'results/001_VRT_videosr_bi_REDS_6frames'
    if modelDict.get('save_result'):
        os.makedirs(save_dir, exist_ok=True)
    test_results = OrderedDict()
    test_results['psnr'] = []
    test_results['ssim'] = []
    test_results['psnr_y'] = []
    test_results['ssim_y'] = []

    len(test_loader) != 0
    print(len(test_loader))

    imagenames = glob.glob('testsets/uploaded/000/*')
    print(type(imagenames))
    for i in imagenames:
        Image.open(i).resize((320,180)).save(i)

    print('s')
    for idx, batch in enumerate(test_loader):
        print('in')
        lq = batch['L'].to(device)
        folder = batch['folder']
        gt = batch['H'] if 'H' in batch else None
    
        with torch.no_grad():
            #print('in')
            output = test_video(lq, model, modelDict)

        test_results_folder = OrderedDict()
        test_results_folder['psnr'] = []
        test_results_folder['ssim'] = []
        test_results_folder['psnr_y'] = []
        test_results_folder['ssim_y'] = []

        for i in range(output.shape[1]):
        # save image
            img = output[:, i, ...].data.squeeze().float().cpu().clamp_(0, 1).numpy()
            if img.ndim == 3:
                img = np.transpose(img[[2, 1, 0], :, :], (1, 2, 0))  # CHW-RGB to HCW-BGR
            img = (img * 255.0).round().astype(np.uint8)  # float32 to uint8
            if modelDict.get('save_result'):
                seq_ = osp.basename(batch['lq_path'][i][0]).split('.')[0]
                os.makedirs(f'{save_dir}/{folder[0]}', exist_ok=True)
                cv2.imwrite(f'{save_dir}/{folder[0]}/{seq_}.png', img)
                print('Working')

        print('Testing {:20s}  ({:2d}/{})'.format(folder[0], idx, len(test_loader)))

    for filename in sorted(glob.glob('/content/VRT/results/001_VRT_videosr_bi_REDS_6frames/000/*')):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
    videoFile = cv2.VideoCapture(filePath)
    framesperSecond = videoFile.get(cv2.CAP_PROP_FPS)
    newVideoFileName = 'finalvideoooempfour.mp4'
    outVideo = cv2.VideoWriter('finalvideoooempfour.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), framesperSecond, size)
    for file in sorted(glob.glob('/content/VRT/results/001_VRT_videosr_bi_REDS_6frames/000/*')):
        imgOne = cv2.imread(file)
        outVideo.write(imgOne)
    cv2.destroyAllWindows()
    outVideo.release()
    path = os.path.join("", newVideoFileName)
    return path
    