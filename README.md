# SullyText: extracting text from the embedded subtitles of a video

I am a big fan of the [Starting Strength](http://www.startingstrength.com) training methodology as well as the forums hosted at http://startingstrength.com/resources/forum/

A recent article on the site, [The Iron Age: Resistance Training and the Metabolic Syndrome](http://startingstrength.com/index.php/site/the_iron_age_resistance_training_and_the_metabolic_syndrome) included a video lecture by Dr. Jonathon Sullivan. In the [resuting discussion](http://startingstrength.com/resources/forum/showthread.php?t=54563) someone asked for a transcript of the talk.

The talk included subtitles embedded in the video, so this is an attempt to create a first draft of a transcript from the subtitles.

The latest raw transcript output is in [transcript.txt](https://raw.githubusercontent.com/kejaed/SullyText/master/transcript.txt).

Work on formatting the trasncript after that is TBD.

So far the experiment is using the following bits and pieces:

* Python (matplotlib, PIL)
* OpenCV
* Tesseract

Screenshot with the GUI turned on:
![Screenshot of code running](https://raw.githubusercontent.com/kejaed/SullyText/master/running.png)
