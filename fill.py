import numpy as np
import cPickle as pickle
import scipy.misc
import visualize as vz
import cv2

# ############################################################ #
#                                                              #
#                       Jonathan Lacombe                       #
#                                                              #
#              CV2 Flood Fill for Annotated Images             #
#                                                              #
# Controls:                                                    #
#                                                              #
# Left Click:  Flood fill at cursor                            #
# Right Click: Draws filled circle at cursor                   #
#                                                              #
# Up:    Next slice                                            #
# Down:  Prev slice                                            #
# Right: Next time frame                                       #
# Left:  Prev time frame                                       #
# E:     Saves all images to /P{}bin                           #
# U:     Loads current slice,frame from /P{}annotation         #
# D:     Prints current slice,frame number                     #   
#                                                              #
# ############################################################ #


# ############################################################ #
#                   MODIFY THESE PARAMETERS                    #
# ############################################################ #

original_dir = "/home/jon-el/Main/CRCV/Spring2017/RV_segmentation/"
patient_id = 16
cursor_diameter = 3

# ############################################################ #



def getPNum(i):
    if (i < 10):
        return "0{}".format(i)
    return i

def getBinaryImages(i,original_dir):
    p = getPNum(i)
        
    x_sub = "P{}/P{}bin/".format(p,p)
    x_dir = original_dir + x_sub

    header = pickle.load(open(x_dir+"header.p","rb"))
    S = header["s"]
    T = header["t"]
    Y = header["y"]
    X = header["x"]

    array_img = []

    SxT = S*T
    for t in range(T):
        sub_array_img = []
        for s in range(S):
            st = s*T + t;
            st4 = format(st,'04')
            ts = t*S + s;
            
            status =  "Patient {} / {} :: ({},{}) {} / {}".format(i,16,t,s,ts,SxT)
            
            x_name = "P{}-{}-{}.png".format(i,s,t)
            x_file = x_dir + x_name
            x_img = scipy.misc.imread(x_file)
            
            sub_array_img.append(x_img)
            
        array_img.append(sub_array_img)
    
    return array_img

def loadAnnotationImage(i,original_dir,s,t):
    p = getPNum(i)
    annotation_sub = "P{}/P{}annotation/".format(p,p)
    annotation_dir = original_dir + annotation_sub
    annotation_name = "P{}-{}-{}.png".format(i,s,t)
    annotation_file = annotation_dir + annotation_name
    annotation_img = scipy.misc.imread(annotation_file)
    return annotation_img

def saveBinaryImage(image,i,original_dir,s,t):
    p = getPNum(i)
    bin_sub = "P{}/P{}bin/".format(p,p)
    bin_dir = original_dir + bin_sub
    bin_name = "P{}-{}-{}.png".format(i,s,t)
    bin_file = bin_dir + bin_name
    scipy.misc.imsave(bin_file, image)




#Cursor Motion Listener
def cursor(event):
    if event.xdata is not None and event.ydata is not None:
        x = int(event.xdata)
        y = int(event.ydata)
        image = np.copy(visualizer.getImage())
        cv2.circle(image,(x,y),cursor_diameter,(255,255,255))
        visualizer.draw(image)
    else:
        visualizer.draw(visualizer.getImage())
    
#Mouse Click Listener
def click(event):
    if event.xdata is not None and event.ydata is not None:
        x = int(event.xdata)
        y = int(event.ydata)
        image = visualizer.getImage()
        if (event.button==1):
            h, w = image.shape[:2]
            mask = np.zeros((h+2, w+2), np.uint8)
            mask[:] = 0
            cv2.floodFill(image,mask,(x,y),(255,255,255))
            visualizer.draw(image)
            visualizer.setImage(image)
        if (event.button==3):
            cv2.circle(image,(x,y),cursor_diameter,(255,255,255),thickness=-1)
            visualizer.draw(image)
            visualizer.setImage(image)
    
#Key Press Listener
def press(event):
    t, s = visualizer.getIndices()
    T, S = visualizer.getShape()
    
    # Undo
    if event.key == 'u':
        image = visualizer.getImage()
        undo = loadAnnotationImage(patient_id,original_dir,s,t)
        np.copyto(image,undo)
        visualizer.draw(image)
        print "Undo performed on ({},{})".format(s,t)
        
    # Save
    if event.key == 'e':
        for tx in range(T):
            for sx in range(S):
                image = visualizer.getImageAt(tx,sx)
                saveBinaryImage(image,patient_id,original_dir,sx,tx)
        print "Saved all binary images for patient: {}".format(patient_id)
        
    # Details
    if event.key == 'd':
        print "Slice, Time : ({},{})".format(s,t)


array_img = getBinaryImages(patient_id, original_dir)

print "Patient: {}".format(patient_id)

visualizer = vz.Visualizer(array_img)
    
visualizer.connect('motion_notify_event',cursor)
visualizer.connect('button_press_event',click)
visualizer.connect('key_press_event',press)

visualizer.show()








