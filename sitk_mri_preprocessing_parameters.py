import numpy as np
import SimpleITK as sitk
import os
from matplotlib import pyplot as plt
from scipy import ndimage

dest = "/home/jon-el/Main/CRCV/Spring2017/RV_preprocess_test/"

PathNii_orig = "/home/jon-el/Main/CRCV/Spring2017/RV_segmentation/"
lstFiles_orig = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathNii_orig):
    for filename in fileList:
		if "dcm" in filename.lower(): 
			lstFiles_orig.append(os.path.join(dirName,filename))
lstFiles_orig.sort()
					
def anisotropic(image_data, it, ts, cp):
	anisotropic = sitk.GradientAnisotropicDiffusionImageFilter()
	anisotropic.SetNumberOfIterations( it )
	anisotropic.SetTimeStep( ts )
	anisotropic.SetConductanceParameter( cp )
	#anisotropic.SetFixedAverageGradientMagnitude(5)
	image_filter = anisotropic.Execute ( image_data )
	return image_filter

def hist_matcher(ref,source, hl, mp):
	hist_match = sitk.HistogramMatchingImageFilter()
	hist_match.SetNumberOfHistogramLevels( hl )
	hist_match.SetNumberOfMatchPoints( mp )
	image_hist_match = hist_match.Execute ( source,ref )
	return image_hist_match

reader = sitk.ImageFileReader()
reader.SetFileName ( lstFiles_orig[0] )
ref = reader.Execute()
float_ref = sitk.Cast(ref,sitk.sitkFloat32)

count = len(lstFiles_orig)
for n in range(count):
    
    itParams = [ 2, 4, 7, 10 ]
    tsParams = [ 0.001, 0.005, 0.01, 0.03 ]
    cpParams = [ 2, 5, 7, 10 ]
    hlParams = [ 100, 500, 800, 1000 ]
    mpParams = [ 5, 15, 50, 100 ]
    
    for it in itParams:
        for ts in tsParams:
            for cp in cpParams:
                for hl in hlParams:
                    for mp in mpParams:
    
                        reader.SetFileName ( lstFiles_orig[n] )
                        source = reader.Execute()
                        orig = reader.Execute()
                        array=sitk.GetArrayFromImage(source)
                        
                        sh=array.shape
                        print "{}_{}_{}_{}_{}".format(it,ts,cp,hl,mp)
                        
                        source = sitk.Cast(source,sitk.sitkFloat32)
                        
                        source=anisotropic(source,it,ts,cp)
                        hist_match=hist_matcher(float_ref,source,hl,mp)
                        
                        #Uncomment one of these extentions
                        ext = ".dcm"
                        #ext = ".png"
                        
                        out_image = None
                        
                        if (ext==".dcm"):
                            out_image = sitk.Cast(hist_match,sitk.sitkUInt16)
                        elif (ext==".png"):
                            out_image = sitk.Cast(hist_match,sitk.sitkUInt8)
                        
                        writer = sitk.ImageFileWriter()
                        fname = dest+"output_{}_{}_{}_{}_{}".format(it,ts,cp,hl,mp)+ext
                        writer.SetFileName ( fname )
                        writer.Execute ( out_image )

    #Only Testing one image
    break


