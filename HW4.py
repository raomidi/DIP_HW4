# Automatic Hole Filling
import cv2
import numpy as np

def threshold(F):
    M = len(F)
    N = len(F[0])
    for i in range(0,M):
        for j in range(0,N):
            if F[i][j] < 255//2:
                F[i][j] = 0
            else:
                F[i][j] = 255
    return F

def intersect(F,G):
    F = F // 255
    G = G // 255
    P = F*G
    return P*255

def dilatePoint(F,x,y):
    B = np.ones((3,3))
    a = (len(B)-1) // 2
    b = (len(B[0]) - 1) // 2
    dilateIt = False

    for s in range(-a, a+1):
        for t in range(-b, b+1):
            try:
                point = F[s+x][t+y]
            except:
                continue

            if point > 0:
                dilateIt = True
                break
        if dilateIt:
            break
    return dilateIt

def dilate(F):
    M = len(F)
    N = len(F[0])
    D = F.copy()

    for i in range(0, M):
        for j in range(0, N):
            if dilatePoint(F,i,j):
                D[i][j] = 255
    return D

def complement(F):
    return 255 - F

def marker(ic):
    M = len(ic)
    N = len(ic[0])
    F = np.zeros((M,N))
    F[0,:] = ic[0,:]
    F[M-1,:] = ic[M-1,:]
    F[:,0] = ic[:,0]
    F[:,N-1] = ic[:,N-1]
    return F

def fillHoles(path):
    # Read input image
    img = cv2.imread(path)
    img = threshold(img[:,:,2])

    # Display original image
    cv2.imshow('Original Image', img)
    cv2.waitKey()

    # Take complement of image
    ic = complement(img)

    # form a marker image F (border of ic)
    F = marker(ic)

    # form a mask as G = Ic(x,y)
    G = ic

    # Perform morphological reconstruction (dilations and intersections)
    k = len(F)//2
    R = intersect(dilate(F),G)
    for i in range(0,k):
        R = intersect(dilate(R),G)

    # Obtain the complement
    R = complement(R)

    cv2.imshow('Hole Filled Image', R)
    cv2.waitKey()
    return
