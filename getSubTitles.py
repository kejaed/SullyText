import sys
import PIL.Image
sys.modules['Image'] = PIL.Image
import Image
import cv2
import pytesseract
import matplotlib.pyplot as plt
import subprocess
import os

#### RUNTIME PARAMETERS ####


# this is where the subtitles start to come in 5730
startFrame = 5730 
#startFrame = 67000

# number of frames to skip each time
skipFrames = 5 

# show the movie and plot metrics or not (much faster when not)
showGUI = 1 ; 


# miminum different number of pixels between frames of text to 
# declare that we have new text
diffValMin = 2000  

# minumum number of non-zero pixels we need in text frame 
# to declare that we have something to decode
nonZeroMin = 100 






# open the video
vid = cv2.VideoCapture('/Users/ken/code/SullyText/video.mp4')

# skip to that frame
vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame); 

# read in the first frame
res,image = vid.read()

# set our frame counter to the frame we're starting at
curFrame = startFrame

lastText = ''
lastVal = 0 
nonZeroList = []
diffValList  = []
allText = ''

# matplotlib interactive mode on, non blocking
plt.ion()

firstTime = 1;


numFrames = vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT);    


c= 'rm /Users/ken/code/SullyText/textImages/*.png' 
print 'Command is', c
subprocess.call(c,shell=True)

while res:
    curFrame = int(vid.get(cv2.cv.CV_CAP_PROP_POS_FRAMES));     

    print "\nFrame: %d / %d " % (curFrame , numFrames)
    
    if showGUI:
        cv2.putText(image, 'Frame ' + str(curFrame),(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),3)
        cv2.imshow('raw',image) 

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #print image.shape
    # note: image is 360,640

    # extract the bottom part with text in it
    textImage = image[278:360,:]

    # display the window
    #cv2.imshow('text',textImage)
   
    # threshold
    rthresh,thresh = cv2.threshold(textImage, 100,255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh',thresh)

    # invert
    inverted = cv2.bitwise_not(thresh)
    if firstTime: 
        lastInverted = inverted.copy()

    if showGUI:
        cv2.imshow('inverted',inverted)
    #print 'countNonZero: ',cv2.countNonZero(thresh) 
    nonZero = cv2.countNonZero(thresh)
    nonZeroList.append(nonZero)
    
    # listen we dont need 2 template, we need the differences between the 2 images
    #templateRes = cv2.matchTemplate(inverted,lastInverted,cv2.TM_CCOEFF)
    #print 'temp res size: ', templateRes.shape
    # sinse we have a template comparison with image of the same size, it's result is going to be 
    #diffVal = templateRes[0,0]
    
    diffInverted = abs(inverted - lastInverted) ; 
    diffVal = cv2.countNonZero(diffInverted)
    diffValList.append(diffVal)

   

    # if the differences between the text frames
    if (diffVal > diffValMin and nonZero > nonZeroMin) or firstTime  :
        
        
        imageFileName = "textImages/%06d.png" % (curFrame,)
        #textFileName = "textImages/%06d.txt" % (curFrame,)
        
        # save the text image to disk
        cv2.imwrite(imageFileName,inverted)


        # run the character recognition on it
        curText = pytesseract.image_to_string(Image.open(imageFileName))
        
        #delete the file we wrote, comment out if we want to debug
        os.remove(imageFileName)

        # replace all newlines with spaces
        curText = curText.replace('\n',' ')

        allText = allText + ' ' + curText 
        print curText
        
        text_file = open("transcript.txt", "w")
        text_file.write("%s" % allText)
        text_file.close()
        
        #text_file = open(textFileName, "w")
        #text_file.write("%s" % curText)
        #text_file.close()
    
    lastInverted = inverted.copy()

    # turn the plot on or off 
    if showGUI:
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
    
    vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, curFrame + skipFrames); 
    
    res,image = vid.read()
    firstTime = 0 ; 


