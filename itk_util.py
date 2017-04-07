import numpy as np
from scipy import ndimage
import SimpleITK as sitk

#dim3 is set to True because reading a dicom image
#   returns an image of shape (1,x,y) when we only
#   need (x,y)
def itkRead(filename,dim3=True):
    reader = sitk.ImageFileReader()
    reader.SetFileName(filename)
    image = reader.Execute()
    if not dim3:
        return image
    return sitk.GetImageFromArray(sitk.GetArrayFromImage(image)[0])
    
def itkWrite(filename,image):
    writer = sitk.ImageFileWriter()
    writer.SetFileName(filename)
    writer.Execute(image)

def cast(source,ext):
    out_image = source
    if (ext==".dcm"):
        out_image = sitk.Cast(source,sitk.sitkUInt32)
    elif (ext==".png"):
        out_image = sitk.Cast(source,sitk.sitkUInt8)
    return out_image

def rescaleRange(array,newMin,newMax):
    min = np.min(array)
    max = np.max(array)
    range = max - min
    newArray = array
    newRange = newMax - newMin
    newArray = newArray - min
    newArray = newArray / float(max)
    newArray = newArray * newRange
    newArray = newArray + newMin
    return newArray

def PNG(source):
    array = sitk.GetArrayFromImage(source)
    array = rescaleRange(array,0,255)
    png_image = sitk.GetImageFromArray(array)
    png_image = cast(png_image,".png")
    return png_image

def load(filename):
    source = itkRead(filename)
    array=sitk.GetArrayFromImage(source)
    return array

def loadRescale(filename, min, max):
    img = load(filename)
    img = rescaleRange(img,min,max)
    return img



