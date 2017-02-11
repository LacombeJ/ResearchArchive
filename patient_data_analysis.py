import numpy as np
import SimpleITK as sitk
import os
from matplotlib import pyplot as plt
from scipy import ndimage
import nibabel as nib


floc = "/home/jon-el/Main/CRCV/Spring2017/Manual_RV_segmentation/Steven_folder/RV_segmentation/"

def analyze(fname):
    img = nib.load(fname)
    shape = img.get_shape()
    x = shape[0]
    y = shape[1]
    t = 20
    s = shape[2] / t
    shape = (s,t,y,x)
    print shape

for i in range(1,10):
    fname = "P0{}.hdr".format(i)
    method(floc+fname)

for i in range(10,17):
    fname = "P{}.hdr".format(i)
    method(floc+fname)
    
    




