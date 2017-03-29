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

print "Performing diff generation"
for i in range(1,17):

    print "Patient {} / {}".format(i,16)
    
    p = getPNum(i)
    
    png_sub = "P{}/P{}png/".format(p,p)
    png_dir = original_dir + png_sub
    
    binary_sub = "P{}/P{}bin/".format(p,p)
    binary_dir = original_dir + binary_sub
    
    diff_sub = "P{}/P{}diff/".format(p,p)
    diff_dir = original_dir + diff_sub
    
    checkOrCreateDir(diff_dir)
    
    header = pickle.load(open(binary_dir+"header.p","rb"))
    S = header["s"]
    T = header["t"]
    Y = header["y"]
    X = header["x"]
    
    for t in range(T):
        for s in range(S):
            st = s*T + t;
            st4 = format(st,'04')
            
            base_name = "P{}-{}-{}".format(i,s,t)
            
            png_name = base_name+".png"
            png_file = png_dir + png_name
            png_img = scipy.misc.imread(png_file)
            
            bin_name = base_name+".png"
            bin_file = binary_dir + bin_name
            bin_img = scipy.misc.imread(bin_file)
            
            diff_name = base_name+".png"
            diff_file = diff_dir + diff_name
            diff_img = bin_img - png_img
            
            scipy.misc.imsave(diff_file, diff_img)
            
print "Done"
        

            

