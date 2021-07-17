# coding=utf-8
import sys
from time import sleep as pause
import scipy.sparse as spr
# import scipy as sci 
import matplotlib.pyplot as plt  
import numpy as np
import cv2

from scipy.stats import norm


from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float


def superpixel_LSC(Im, region_size, ruler, iter_num, min_size):
    
    cv2.ximgprm_height = Im.shape[0]
    m_width = Im.shape[1]
    m_channels = Im.shape[2]

    bins_n = int(m_channels/3)
    bins_r = Im[:, :, 0:bins_n]
    bins_g = Im[:, :, bins_n:2*bins_n]
    bins_b = Im[:, :, 2*bins_n:m_channels]

    bins_r = np.exp( np.mean( np.log(bins_r),2))
    bins_r_ = np.zeros(0)
    bins_r = cv2.normalize(bins_r , bins_r_, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    bins_g = np.exp( np.mean( np.log(bins_g),2))
    bins_g_ = np.zeros(0)
    bins_g = cv2.normalize(bins_g , bins_g_, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    bins_b = np.exp( np.mean( np.log(bins_b),2))
    bins_b_ = np.zeros(0)
    bins_b = cv2.normalize(bins_b , bins_b_, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


    img = np.concatenate([bins_r[:,:,np.newaxis],bins_g[:,:,np.newaxis], bins_b[:,:,np.newaxis]], 2)

    retval = cv2.ximgproc.createSuperpixelLSC(img, int(region_size), float(ruler)) 
 
    retval.iterate(int(iter_num))
    retval.enforceLabelConnectivity(int(min_size))
    
    segments_LSC=retval.getLabels()

    sup_map =  mark_boundaries(img,segments_LSC)
    sup_map = np.uint8(sup_map*255)
##    plt.figure("SLIC superpixel map")
##    plt.imshow(mark_boundaries(img,segments_MSLIC))
##    plt.axis('off')
##    plt.show()

    print("segmented with ", np.max(segments_LSC)+1, " superpixels")
    return sup_map

    


