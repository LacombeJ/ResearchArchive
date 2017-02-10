import numpy as np
import SimpleITK as sitk
import os
from matplotlib import pyplot as plt
from scipy import ndimage

dest = "/home/jon-el/Main/CRCV/Spring2017/RV_preprocess/"

PathNii_orig = "/home/jon-el/Main/CRCV/Spring2017/RV_segmentation/"
lstFiles_orig = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathNii_orig):
    for filename in fileList:
		if "dcm" in filename.lower(): 
			lstFiles_orig.append(os.path.join(dirName,filename))
lstFiles_orig.sort()
					
def anisotropic(image_data):
	anisotropic = sitk.GradientAnisotropicDiffusionImageFilter()
	anisotropic.SetNumberOfIterations( 7)
	anisotropic.SetTimeStep( 0.03 )
	anisotropic.SetConductanceParameter( 5 )
	#anisotropic.SetFixedAverageGradientMagnitude(5)
	image_filter = anisotropic.Execute ( image_data )
	return image_filter

def hist_matcher(ref,source):
	hist_match = sitk.HistogramMatchingImageFilter()
	hist_match.SetNumberOfHistogramLevels( 500)
	hist_match.SetNumberOfMatchPoints( 100 )
	image_hist_match = hist_match.Execute ( source,ref )
	return image_hist_match

reader = sitk.ImageFileReader()
reader.SetFileName ( lstFiles_orig[0] )
ref = reader.Execute()
float_ref = sitk.Cast(ref,sitk.sitkFloat32)

count = len(lstFiles_orig)
for n in range(count):
    
    reader.SetFileName ( lstFiles_orig[n] )
    source = reader.Execute()
    orig = reader.Execute()
    array=sitk.GetArrayFromImage(source)
    
    sh=array.shape
    print str(n)+"/"+str(count), lstFiles_orig[n], sh
    
    source = sitk.Cast(source,sitk.sitkFloat32)
    
    source=anisotropic(source)
    hist_match=hist_matcher(float_ref,source)
    
    #Uncomment one of these extentions
    ext = ".dcm"
    #ext = ".png"
    
    out_image = None
    
    if (ext==".dcm"):
        out_image = sitk.Cast(hist_match,sitk.sitkUInt16)
    elif (ext==".png"):
        out_image = sitk.Cast(hist_match,sitk.sitkUInt8)
    
    writer = sitk.ImageFileWriter()
    fname = dest+"output_"+str(n)+ext
    writer.SetFileName ( fname )
    writer.Execute ( out_image )



