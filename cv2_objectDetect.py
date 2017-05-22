import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tkinter import *
from time import ctime
import openCVLib
import web_streaming
from threading import Thread

def capture_single_frame(cap):
	ret , color_frame = cap.read()
	hsv_frame =cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV) # changing color to HSV format
	
	mask = openCVLib.color_filter(hsv_frame,'orange')
	smoothed_frame = openCVLib.smooth(mask, 2, 10)
	
	smoothed= smoothed_frame.copy()
	(contours,hier)= cv2.findContours(smoothed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	frame, x, y = openCVLib.draw_contour(cap.read()[1], contours, 'rect') 
	return frame, x, y
	
	
	
def Detect():
	color = (255,255,25)
	cap= cv2.VideoCapture(0)
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	out = cv2.VideoWriter('/home/pi/Desktop/rpi3/openCV/orange_detect.avi', fourcc, 10.0, (640,480))
	t = Thread(target = web_streaming.main,args=(cap,))
	t.start()
	debugMode = True
	
	while True:
		frame, x, y = capture_single_frame(cap)
		string = "Orange object detected  " + "x="+str(x) + "y="+str(y)
		date = ctime()		
		if (x!= -1 and y!= -1):
			frame = openCVLib.write_frame(frame, string, date, color)
			out.write(frame)
		
		if (debugMode == True):
			cv2.rectangle(frame,(160,120),(480,360), (0,0,0),1)
			cv2.imshow("cunt",frame)
		
		k = (cv2.waitKey(1) & 0xFF) 
		if k == ord('q'):
			break
		if k == ord('d'):
			print ("Turning on DebugMode")
			debugMode = not debugMode 
			

	
	print "releasing"	
	cap.release()
	out.release()
	cv2.destroyAllWindows


if __name__ == '__main__':
    Detect()
	






"""


def read(self):

	lh_max.config(text= "hue max = " + str(h_max.get()))
	ls_max.config(text= "saturation max = " + str(s_max.get()))
	lv_max.config(text= "value max = " + str(v_max.get()))
	
	lh_min.config(text= "hue min= " + str(h_min.get()))
	ls_min.config(text= "saturation min= " + str(s_min.get()))
	lv_min.config(text= "value min= " + str(v_min.get()))
	
	lower_blue = np.array([lh_min,ls_min,lv_min])
	upper_blue = np.array([lh_max,ls_max,lv_max])
	
	
master = Tk()

h_max = Scale(master, from_=0, to=179, orient = HORIZONTAL, command = read)
lh_max = Label(master)

s_max = Scale(master, from_=0, to=255, orient = HORIZONTAL, command = read)
ls_max = Label(master)

v_max = Scale(master, from_=0, to=255, orient = HORIZONTAL, command = read)
lv_max = Label(master)

h_min = Scale(master, from_=0, to=179, orient = HORIZONTAL, command = read)
lh_min = Label(master)

s_min = Scale(master, from_=0, to=255, orient = HORIZONTAL, command = read)
ls_min = Label(master)

v_min = Scale(master, from_=0, to=255, orient = HORIZONTAL, command = read)
lv_min = Label(master)

h_max.pack()
lh_max.pack()
s_max.pack()
ls_max.pack()
v_max.pack()
lv_max.pack()

h_min.pack()
lh_min.pack()
s_min.pack()
ls_min.pack()
v_min.pack()
lv_min.pack()


master.mainloop()

"""


