import os.path
import numpy as np
import sys

def nextFilename(name):
    m = 0
    filename = "{}_{}.txt".format(name,m)
    while True:
        filename = "{}_{}.txt".format(name,m)
        if os.path.isfile(filename):
            m = m+1
        else:
            break
    return filename

def writeMatrix(file,M):
    r = M.shape[0]
    file.write("{}\n".format(r))
    for col in M:
        for e in col:
            file.write("{} ".format(e))
        file.write("\n")

def readMatrix(file,M):
    r = int(file.readline())
    for i in range(r):
        tokens = file.readline().split()
        row = []
        for e in tokens:
            row.append(float(e))
        M.append(row)

def saveWeights(fname,W,b):
    with open(fname,"w") as file:
        writeMatrix(file,W)
        writeMatrix(file,b)

def loadWeights(fname):
    W = []
    b = []
    with open(fname,"r") as file:
        readMatrix(file,W)
        readMatrix(file,b)
    return W,b

def writeLabel(file,label,M):
    for row in M:
        file.write("{} ".format(label))
        for e in row:
            file.write("{} ".format(e))
        file.write("\n")

def readLabel(file,L,M):
    for line in file:
        tokens = line.split()
        for i, l in enumerate(L):
            if tokens[0] == l:
                row = tokens[1:]
                build = []
                for e in row:
                    build.append(float(e))
                M[i].append(build)

def saveLabels(fname,L,M):
    with open(fname,"w") as file:
        for i, l in enumerate(L):
            writeLabel(file,l,M[i])

def loadLabels(fname,L):
    M = [[] for i in L]
    with open(fname,"r") as file:
        readLabel(file,L,M)
    return M

def take_all(id):
    return True

def take_one(id):
    return id == "1"

def take_none(id):
    return id == "0"

def resetMinMax():
    min = 2**16
    max = 0

def normalize(M):
    return (M - min) / (max - min)

def prepareUpdate():
    global mlen
    mlen = 0

def printUpdate(str):
    global mlen
    if len(str) < mlen:
        str = str + ' '*(len(str)-mlen)
    elif len(str) > mlen:
        mlen = len(str)
    sys.stdout.write('\r'+str)
    sys.stdout.flush()

'''
def loadData(f,patches):
    global min, max
    X = []
    for i in patches:
        with open("patches/patchxy{}.txt".format(i),"r") as file:
            for line in file:
                tokens = line.split()
                if f(tokens[0]):
                    array = []
                    for i in tokens[1:]:
                        v = int(i)
                        if v < min: min = v
                        if v > max: max = v
                        array.append(v)
                    X.append(array)
    X = np.float32(X)
    return X
'''





