import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import ctime
import openCVLib
from web_streaming import WebStreamer
from threading import Thread


def capture_succ_frames(cap):
	t_minus = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
	t = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
	t_plus = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
	smooth_diff_frame = openCVLib.diffImg(t_minus,t,t_plus)
	
	smoothed= smooth_diff_frame.copy()
	(contours,hier)= cv2.findContours(smoothed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	frame, x, y = openCVLib.draw_contour(cap.read()[1], contours, 'rect')
	return frame, x, y
	
	


def Track():
	color = (25,25,2180)
	cap= cv2.VideoCapture(0)
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	out = cv2.VideoWriter('/home/igor/tmp/motion_detect.avi', fourcc, 10.0, (640,480))
	web_streaming = WebStreamer(cap)
	web_streaming.start()
	debugMode = True
	
	print ('first t sec not processed')
	openCVLib.discard_t_sec(cap,5)
	print('camera armed  to detect motion')
	try:
		while True:
			frame, x, y = capture_succ_frames(cap)
			string = "Motion detected  " + "x="+str(x) + "y="+str(y)
			date = ctime()
			if (x!= -1 and y!= -1):
				frame = openCVLib.write_frame(frame, string, date , color)
				out.write(frame)
				
			if (debugMode == True):
				cv2.imshow("cunt",frame)
			
			k = (cv2.waitKey(1) & 0xFF) 
			if k == ord('q'):
				break
			if k == ord('d'):
				print ("Toggling DebugMode")
				debugMode = not debugMode 
	except KeyboardInterrupt:
		web_streaming.stop()
	
	#cv2.imwrite('bw_me.png',gray)
	#cv2.imwrite('color_me.png',frame)
	print("destroying windows")
	cap.release()
	print("destroying windows")
	out.release()
	print("destroying windows")
	cv2.destroyAllWindows


if __name__ == '__main__':
    Track()
	
