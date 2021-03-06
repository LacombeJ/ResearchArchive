import numpy as np
import SimpleITK as sitk
import itk_util as itk
import os
from matplotlib import pyplot as plt
from scipy import ndimage
from scipy import stats
import nibabel as nib
import cPickle as pickle
import scipy.misc
import myutil as mu

original_dir = "/home/jon-el/Main/CRCV/Spring2017/RV_segmentation/"
annotation_dir = "/home/jon-el/Main/CRCV/Spring2017/Manual_RV_segmentation/Steven_folder/RV_segmentation/"

#Flip y - hdr files are upside down for some reason?
def changeShape(img):
    shape = img.shape
    x = shape[0]
    y = shape[1]
    t = 20
    s = shape[2] / t
    ret = np.zeros(s*t*y*x).reshape((s,t,y,x))
    for X in range(x):
        for Y in range(y):
            for S in range(s):
                for T in range(t):
                    st = S*t + T
                    ret[S,T,y-1-Y,X] = img[X,Y,st,0]
    return ret

def getPNum(i):
    if (i < 10):
        return "0{}".format(i)
    return i

def checkOrCreateDir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
def getDiff(A,B):
    diff = np.abs(A - B)
    return diff
    
def binary(image):
    result = stats.threshold(image, threshmin=0, threshmax=None, newval=255)
    #result = stats.threshold(result, threshmin=0, threshmax=None, newval=1)
    return result

mu.prepareUpdate()
print "Performing Binary Transformation"
for i in range(1,17):
    #print "Patient {} / {}".format(i,16)
    
    p = getPNum(i)
    
    original_sub = "P{}/P{}dicom/".format(p,p)
    binary_sub = "P{}/P{}bin/".format(p,p)
    binary_dir = original_dir + binary_sub
    
    checkOrCreateDir(binary_dir)
    
    annotation_name = "P{}.hdr".format(p)
    annotation_file = annotation_dir + annotation_name
    annotation = nib.load(annotation_file)
    
    img3d = annotation.get_data()
    img4d = changeShape(img3d)
    shape4d = img4d.shape
    
    S,T,Y,X = shape4d
    header = { "s":S, "t":T, "y":Y, "x":X }
    
    pickle.dump(header, open(binary_dir+"header.p","wb"))
    
    SxT = S*T
    for t in range(T):
        for s in range(S):
            st = s*T + t;
            st4 = format(st,'04')
            ts = t*S + s;
            
            status =  "Patient {} / {} :: ({},{}) {} / {}".format(i,16,t,s,ts,SxT)
            
            binary_name = "P{}-{}-{}.png".format(i,s,t)
            binary_file = binary_dir + binary_name
            
            img2d = img4d[s,t]
            
            original_name = "P{}-{}.dcm".format(p,st4)
            original_file = original_dir + original_sub + original_name
            original = itk.load(original_file)
            
            diff = getDiff(img2d,original)
            bin_img = binary(diff)
            
            scipy.misc.imsave(binary_file, bin_img)
            
            mu.printUpdate(status)
            
print ""
print "Done"

