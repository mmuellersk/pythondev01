#!/usr/bin/env python

import numpy
import cv2

def hasAlphaChanel(image):
    return image.shape[2] == 4

def transformAlpha2White(image):
    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            if image.item(x,y,3) == 0 :
                image.itemset((x,y,0),255)
                image.itemset((x,y,1),255)
                image.itemset((x,y,2),255)
                image.itemset((x,y,3),255)
    return cv2.cvtColor(image,cv2.COLOR_RGBA2RGB)

def transformWhite2Alpha(image):
    if image.shape[2] == 3:
        image = cv2.cvtColor(image,cv2.COLOR_RGB2RGBA)
    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            if image.item(x,y,0) == 255 and image.item(x,y,1) == 255 and image.item(x,y,2) == 255:
                image.itemset((x,y,3),0)
    return image

def transformBlack2Alpha(image, mask):
    if len(mask.shape) != 2:
        print('Error: transformBlack2Alpha mask is not gray image')
        return image
        
    if image.shape[2] == 3:
        image = cv2.cvtColor(image,cv2.COLOR_RGB2RGBA)
    for x in range(0, mask.shape[0]):
        for y in range(0, mask.shape[1]):
            if mask.item(x,y) == 0:
                image.itemset((x,y,3),0)
    return image
