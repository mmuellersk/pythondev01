#!/usr/bin/env python
import os
import numpy
import cv2
import svgwrite
import base64

from core.imglib import *

class ContouringFilter :
    def __init__( self, filename, outputfolder ):
        self.padding = 100
        self.thresholdInit = 254
        self.opening = 20
        self.dilate = 30
        self.blur = 40
        self.threseholdBlur = 130

        self.filename = filename
        self.outputfolder = outputfolder

        self.imgwidth = 100
        self.imgheight = 100

        self.basename = os.path.basename(self.filename).rsplit(".", 1)[0]
        print(self.basename)

        self.inputimg = None
        self.contour = None

    def processImage(self):

        # read input image
        self.inputimg = cv2.imread(self.filename,cv2.IMREAD_UNCHANGED)
        self.originalimg = self.inputimg.copy()
        if hasAlphaChanel(self.inputimg) :
            inputimg = transformAlpha2White(self.inputimg)

        self.imgwidth = inputimg.shape[1]
        self.imgheight = inputimg.shape[0]

        # make image bigger
        borderimg = cv2.copyMakeBorder(self.inputimg,
            self.padding,self.padding,self.padding,self.padding,
            cv2.BORDER_CONSTANT,value=[255,255,255])

        # to grayscale
        grayimg = cv2.cvtColor(borderimg,cv2.COLOR_RGB2GRAY)

        # initial thresehold
        ret,thresholdimg = cv2.threshold(grayimg,
            self.thresholdInit,255,cv2.THRESH_BINARY)

        # opening
        openingkernel = numpy.ones((self.opening,self.opening),numpy.uint8)
        openingimg = cv2.morphologyEx(thresholdimg, cv2.MORPH_OPEN, openingkernel)

        # dilatation
        dilatekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
            (self.dilate,self.dilate))
        invertedimg = cv2.bitwise_not(openingimg)
        dilationimg = cv2.dilate(invertedimg,dilatekernel,iterations = 2)

        # blur and threshold
        blurimg = cv2.blur(dilationimg,(self.blur,self.blur))
        ret,finalbinaryimg = cv2.threshold(blurimg,self.threseholdBlur,255,cv2.THRESH_BINARY)

        # get and draw contours
        contourimg, contours, hierarchy = cv2.findContours(finalbinaryimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contourimg = cv2.drawContours(borderimg, contours, 0, (0,255,0), 2)

        self.contour = contours[0]

        outputfilename = os.path.join(self.outputfolder,self.filename.rsplit("/", 1)[-1])


    def writeSVG(self):

        dwg = svgwrite.Drawing(self.basename+'.svg',
            size=(self.imgwidth + 2*self.padding,self.imgheight + 2*self.padding),
            profile = 'tiny')

        polyline = []
        for elem in self.contour:
            polyline.append((str(elem[0][0]),str(elem[0][1])))

        contouringLayer = dwg.add( dwg.g(id='cutting') )
        contouringLayer.add(dwg.polygon(polyline, stroke='red', stroke_width=1, fill='none'))


        encoded = base64.b64encode(open(self.filename, "rb").read()).decode()

        imageLayer = dwg.add( dwg.g(id='image') )
        imageLayer.add(dwg.image(href='data:image/png;base64,{}'.format(encoded),insert=(self.padding,self.padding)))

        outputfilename = os.path.join(self.outputfolder,self.basename+'.svg')

        dwg.saveas(outputfilename)
