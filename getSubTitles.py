import cv2

# open the video
vid = cv2.VideoCapture('/Users/ken/code/SullysText/video.mp4')

# this is where the subtitles start to come in 5730
startFrame = 5730 

# skip to that frame
vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame); 

# read in the first frame
res,image = vid.read()

# set our frame counter to the frame we're starting at
curFrame = startFrame

# while we still have good video
while res:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #print image.shape
    # image is 360,640

    # extract the bottom part with text in it
    textImage = image[275:360,:]

    # display the window
    cv2.imshow('text',textImage)
    print "Frame: ",curFrame
   
    # threshold

    # compare to last one

    # if it's different enough, declare new text and do OCR on it
    # review the link from https://news.ycombinator.com/item?id=8912219
    # which is http://www.danvk.org/2015/01/09/extracting-text-from-an-image-using-ocropus.html
    
    # stop if someone presses escape
    key = cv2.waitKey(100)
    if key  == 27:
        print "exiting!"
        break
    res,image = vid.read()
    curFrame = curFrame + 1


