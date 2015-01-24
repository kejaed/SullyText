

import sys
import PIL.Image
sys.modules['Image'] = PIL.Image

import Image


import cv2
import pytesseract
import matplotlib.pyplot as plt

# open the video
vid = cv2.VideoCapture('/Users/ken/code/SullyText/video.mp4')

# this is where the subtitles start to come in 5730
startFrame = 5730 
#startFrame = 7500

# skip to that frame
vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame); 

# read in the first frame
res,image = vid.read()

# set our frame counter to the frame we're starting at
curFrame = startFrame

lastText = ''
lastVal = 0 
# while we still have good video

nonZeroList = []
diffValList  = []

# matplotlib interactive mode on, non blocking
plt.ion()


while res:
        
    #print "\nFrame: ",curFrame

    cv2.putText(image, 'Frame ' + str(curFrame),(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
    cv2.imshow('raw',image) 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #print image.shape
    # note: image is 360,640

    # extract the bottom part with text in it
    textImage = image[277:360,:]

    # display the window
    #cv2.imshow('text',textImage)
   
    # threshold
    rthresh,thresh = cv2.threshold(textImage, 100,255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh',thresh)

    # invert
    inverted = cv2.bitwise_not(thresh)
    if curFrame == startFrame:
        lastInverted = inverted.copy()

    #cv2.imshow('inverted',inverted)
    #print 'countNonZero: ',cv2.countNonZero(thresh) 
    nonZeroList.append(cv2.countNonZero(thresh))
    
    # listen we dont need 2 template, we need the differences between the 2 images
    #templateRes = cv2.matchTemplate(inverted,lastInverted,cv2.TM_CCOEFF)
    #print 'temp res size: ', templateRes.shape
    # sinse we have a template comparison with image of the same size, it's result is going to be 
    #diffVal = templateRes[0,0]
    
    diffInverted = abs(inverted - lastInverted) ; 
    diffVal = cv2.countNonZero(diffInverted)
    diffValList.append(diffVal)

    if curFrame != startFrame:
        #templateRes = cv2.matchTemplate(inverted,lastInverted,cv2.TM_CCOEFF)
        #min_val, diffVal, min_loc, max_loc = cv2.minMaxLoc(templateRes)

        if abs(lastVal - diffVal) > 100000000 and  diffVal > 10000:
            #print 'I think we should use the last text now'
            cv2.imwrite('out.png',inverted)
            curText = pytesseract.image_to_string(Image.open('out.png'))
            curText = curText.replace('\n','')
            print 'diffVal: ', diffVal
            print 'abs: ', abs(lastVal -diffVal)
            print curText
            print len(curText)
            lastText = curText
        lastInverted = inverted.copy()
        lastVal = diffVal
    else:
        lastInverted = inverted.copy()

    #if curText != lastText:
    #    print curText
    #    lastText = curText
    
    if 1:
        plt.figure(1)
        plt.clf()
        plt.subplot(211)
        plt.plot(diffValList)
        plt.title('diffValList')
        plt.subplot(212)
        plt.plot(nonZeroList)
        plt.title('nonZeroList')
        #plt.draw()



    # stop if someone presses escape
    key = cv2.waitKey(100)
    if key  == 27:
        print "exiting!"
        break
    res,image = vid.read()
    curFrame = curFrame + 1


