import numpy as np
import itk_util as itk
import os
from matplotlib import pyplot as plt
from scipy import ndimage
import nibabel as nib
import cPickle as pickle
import scipy.misc

original_dir = "/home/jon-el/Main/CRCV/Spring2017/RV_segmentation/"

def getPNum(i):
    if (i < 10):
        return "0{}".format(i)
    return i

def checkOrCreateDir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

print "Performing PNG Transformation"
for i in range(1,17):

    print "Patient {} / {}".format(i,16)
    
    p = getPNum(i)
    original_sub = "P{}/P{}dicom/".format(p,p)
    png_sub = "P{}/P{}png/".format(p,p)
    png_dir = original_dir + png_sub
    
    checkOrCreateDir(png_dir)
    
    binary_sub = "P{}/P{}bin/".format(p,p)
    binary_dir = original_dir + binary_sub
    
    header = pickle.load(open(binary_dir+"header.p","rb"))
    S = header["s"]
    T = header["t"]
    Y = header["y"]
    X = header["x"]
    
    for t in range(T):
        for s in range(S):
            st = s*T + t;
            st4 = format(st,'04')
            
            original_name = "P{}-{}.dcm".format(p,st4)
            original_file = original_dir + original_sub + original_name
            original = itk.load(original_file)
            
            png_name = "P{}-{}-{}.png".format(i,s,t)
            png_file = png_dir + png_name
            scipy.misc.imsave(png_file, original)
            
print "Done"
        

            

