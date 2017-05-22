# openCV-python-webserver
Python program for raspberry pi to use a webcam to track/detect motion, write video file and also stream video


This repo has 2 main programs 1a and 1b
1.  a. track object depending on color to track -> cv2_objectDetect.py
    b. motion detect to detect any motion in the frame -> cv2_tracking.py 
2.create a webserver to view video from internet (struggling with this part as my knowledge in HTTP webserver protocol is pretty terrible). Both programs in 1a and 1b call web_streaming.py to do this. Currently cant kill this webserver externally.
3. Write to video files when orange object is detected (1a) or motion is detected (1b)


