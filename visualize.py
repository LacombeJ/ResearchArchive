#Jonathan Lacombe
#Visualizing weights utility

import numpy as np
from matplotlib import pyplot as plt


class Visualizer(object):

    def __init__(self,
    images):
        self._images = np.array(images)
        self._shape0 = self._images.shape[0]
        self._shape1 = self._images.shape[1]
        self._index0 = 0
        self._index1 = 0
        
        self._fig, self._ax = plt.subplots()
        
        self._events = []
        self._keyPressEvent = self._fig.canvas.mpl_connect('key_press_event', self._keyPress)
        self._events.append(self._keyPressEvent)
        
    def _keyPress(self,event):
        if event.key == 'left' and self._index0 > 0:
            self._index0 = self._index0 - 1
        if event.key == 'right' and self._index0 < self._shape0-1:
            self._index0 = self._index0 + 1

        if event.key == 'down' and self._index1 > 0:
            self._index1 = self._index1 - 1
        if event.key == 'up' and self._index1 < self._shape1-1:
            self._index1 = self._index1 + 1
            
        self.draw( self.getImage() )
        
    def show(self):
        self._imshow = plt.imshow(self._images[0][0],cmap='gray')
        plt.show()
        
    def connect(self,name,event):
        canvasEvent = self._fig.canvas.mpl_connect(name, event)
        self._events.append(canvasEvent)
        return canvasEvent
        
    def getImage(self):
        return self._images[self._index0,self._index1]
        
    def getImageAt(self,i0,i1):
        return self._images[i0,i1]
        
    def setImage(self,image):
        self._images[self._index0,self._index1] = image
        
    def getShape(self):
        return self._shape0, self._shape1
        
    def getIndices(self):
        return self._index0, self._index1
        
    def draw(self,image):
        self._imshow.set_data(image)
        self._fig.canvas.draw()
        
def saveWeights(W,fname):
    with open(fname,"w") as file:
        for row in W:
            for e in row:
                file.write("{} ".format(e))
            file.write("\n")

def loadWeights(fname):
    with open(fname,"r") as file:
        W = []
        for line in file:
            row = []
            tokens = line.split()
            for token in tokens:
                row.append(float(token))
            W.append(row)
        return np.array(W)

def visualize(W,col,w,h):
    n = col
    row = W.shape[0]/col
    plt.figure(figsize=(60, 36))
    for i in range(len(W)):
        ax = plt.subplot(row, n, i + 1)
        plt.imshow(W[i].reshape(w,h))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()

def keyPress(event):
    global fig, images, width, height, sIndex, tIndex, slices, time, ims
    if event.key == 'left' and tIndex > 0:
        tIndex = tIndex - 1

    if event.key == 'right' and tIndex < time-1:
        tIndex = tIndex + 1

    if event.key == 'down' and sIndex > 0:
        sIndex = sIndex - 1
        
    if event.key == 'up' and sIndex < slices-1:
        sIndex = sIndex + 1

    if event.key == 'q':
        print ('slice:',sIndex,'time:',tIndex)

    for i, image in enumerate(images):
        ims[i].set_data(image[sIndex][tIndex])

    fig.canvas.draw()

def visualize4d(images4d):
    global fig, images, sIndex, tIndex, slices, time, width, height, ims
    images = images4d
    
    sIndex = 0
    tIndex = 0
    slices, time, height, width = images[0].shape
    fig, ax = plt.subplots()
    cidKP = fig.canvas.mpl_connect('key_press_event', keyPress)

    ims = []
    for i, image in enumerate(images):
        plt.subplot(1,len(images),i+1)
        ims.append(plt.imshow(image[0][0],'gray'))

    plt.show()




