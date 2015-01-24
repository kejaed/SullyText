import Image
import cv2
import pytesseract

# open the video
vid = cv2.VideoCapture('/Users/ken/code/SullyText/video.mp4')

# this is where the subtitles start to come in 5730
startFrame = 5730 
startFrame = 7500

# skip to that frame
vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame); 

# read in the first frame
res,image = vid.read()

# set our frame counter to the frame we're starting at
curFrame = startFrame

lastText = ''
lastVal = 0 
# while we still have good video
while res:
    print "\nFrame: ",curFrame
    cv2.imshow('raw',image) 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #print image.shape
    # image is 360,640

    # extract the bottom part with text in it
    textImage = image[277:360,:]

    # display the window
    #cv2.imshow('text',textImage)
   
    # threshold
    rthresh,thresh = cv2.threshold(textImage, 100,255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh',thresh)

    # invert
    inverted = cv2.bitwise_not(thresh)
    #cv2.imshow('inverted',inverted)
    print 'countNonZero: ',cv2.countNonZero(thresh) 

    if curFrame != startFrame:
        templateRes = cv2.matchTemplate(inverted,lastInverted,cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(templateRes)
        if abs(lastVal - max_val) > 100000000 and  max_val > 10000:
            #print 'I think we should use the last text now'
            cv2.imwrite('out.png',inverted)
            curText = pytesseract.image_to_string(Image.open('out.png'))
            curText = curText.replace('\n','')
            print 'max_val: ', max_val
            print 'abs: ', abs(lastVal -max_val)
            print curText
            print len(curText)
            lastText = curText
        lastInverted = inverted.copy()
        lastVal = max_val
    else:
        lastInverted = inverted.copy()

    #if curText != lastText:
    #    print curText
    #    lastText = curText



    # compare to last one

    # if it's different enough, declare new text and do OCR on it
    # review the link from https://news.ycombinator.com/item?id=8912219
    # which is http://www.danvk.org/2015/01/09/extracting-text-from-an-image-using-ocropus.html
    
    # stop if someone presses escape
    key = cv2.waitKey(100)
    #if key  == 27:
    #    print "exiting!"
    #    break
    res,image = vid.read()
    curFrame = curFrame + 1


