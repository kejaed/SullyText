# SullyText: extracting text from the embedded subtitles of a video

I am a big fan of the [Starting Strength](http://www.startingstrength.com) training methodology as well as the forums hosted at http://startingstrength.com/resources/forum/

A recent article on the site, [The Iron Age: Resistance Training and the Metabolic Syndrome](http://startingstrength.com/index.php/site/the_iron_age_resistance_training_and_the_metabolic_syndrome) included a video lecture by Dr. Jonathon Sullivan. In the [resulting discussion](http://startingstrength.com/resources/forum/showthread.php?t=54563) someone asked for a transcript of the talk.

The talk included subtitles embedded in (most of) the video, so this is an attempt to create a first draft of a transcript from the subtitles. The engineer in me just couldn't resist.

When the program is run, it creates an output file with one big long block of text. The latest output from the program is in [transcript.txt](https://raw.githubusercontent.com/kejaed/SullyText/master/transcript.txt). This raw output is of little use to anyone.

To create something of some usefulness, I have started to format the transcript in a Google Doc.

https://docs.google.com/document/d/1jCoMCCBY5VWUHY01jVSioqyrMCTInY3x2lLy2Aaox-I/edit?usp=sharing

If you would like to help with the formatting of the transcript, please email me at ken@kje.ca

Some notes:
* There is a long stretch in the middle of the video (the literature-review section) with no in-line subtitles. This part of the Google Doc transcript was trasnscribed by hand from the audio of the talk. Any errors in here are obviously mine. Please send fixes to the above address or submit a pull request if you know what that means.
* In the code, the default values for parameters that detect a change in the text (diffValMin, nonZeroMin )are probably too high, some text that was displayed in the video is missing from the transcript. Mostly very short pieces of text or, as an educated guess, text with a very similar number of white pixels as the last screen of text. I had switched from a template matching score to a frame different score, and it looks like this might have been a case of premature optimization. However, it was not bad enough to re-run the script and start the eddited transcription file over. 

As for the code, the experiment is using the following bits and pieces:

* Python (matplotlib, PIL)
* OpenCV
* Tesseract

Screenshot with the GUI turned on:
* "raw": the raw frame from the video with the frame number added in red
* "inverted": the black-background text portion of the frame has each pixel inverted
* "Figure 1": plotting of two metrics that look at the text
** diffValList: taking two consecutive frames and subtracting one from the other, this is the number of non-zero pixels, or, the number of pixels that are different between the two frames.
** nonZeroList: the number of non-zero pixels in the black-background frame. This is the number of pixels of text in the frame
* Top right screen: contains the output of the program running, which is the detected text from each frame
* "getSubTitles.py": the code editor 
![Screenshot of code running](https://raw.githubusercontent.com/kejaed/SullyText/master/running.png)
