import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tkinter import *





cap= cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('/home/pi/Desktop/rpi3/move.avi', fourcc, 20.0, (640,480))

kernel_erode = np.ones((2,2),np.uint8)
kernel_dilate = np.ones((10,10),np.uint8)
kernel = np.ones((15,15),np.float32)/225

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_orange = np.array([0,150,210])
upper_orange = np.array([44,291,286])

while True:		
	ret , color_frame = cap.read()
	hsv_frame =cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV) # changing color to HSV format
	
	#creating a mask to filter only orange, if any pixel falls in the range, it will be white
	#And this mask basically can be used for all purposes. It is 0 or 255 image with white 
	#as anywhere it matched the color window
	mask = cv2.inRange(hsv_frame,lower_orange, upper_orange)
	#cv2.imshow('mask',mask)
	
	"""
	#filtering the orange. when white from mask ANDs with orange of hsv_frame, it will be orange
	#and everything else will be black
	res_frame = cv2.bitwise_and(hsv_frame, hsv_frame, mask = mask)
	#cv2.imshow('res',res_frame)
	
	
	#splitting the matrix into its components because i only need the gray which is similar to value array
	#h,s,gray_frame = cv2.split(res_frame) 
	#cv2.imshow('gray',gray_frame)
	
	#below are different ways to blur. Median blur seems to be the best
	
	smoothed = cv2.filter2D(gray_frame, -1, kernel)
	cv2.imshow('smooth',smoothed)
	blur = cv2.GaussianBlur(gray_frame, (15,15), 0)
	cv2.imshow('blur',blur)
	
	median = cv2.medianBlur(gray_frame, 15)
	cv2.imshow('median',median)
	"""
	
	#eroding the edges to smoothen the pictures by eroding the boundaries, 
	#use the kernel to do this 
	erosion = cv2.erode(mask, kernel_erode, iterations =1)
	
	#expand the pixels inside the orange object that I want to track
	#used because sometimes there are holes inside a full object. this will make it whole
	dilation= cv2.dilate(erosion, kernel_dilate, iterations =1)
	#cv2.imshow('dilation',dilation)	
	
	"""
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	#cv2.imshow('open',opening) #removes false negative. removes white in the background
	cv2.imshow('close',closing) #removes false positives. removes holes within the object

	closing = closing.copy()
	"""
	dilation = dilation.copy()
	(contours,hier)= cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	
    #for contour in contours:
	#cv2.drawContours(color_frame, contours, -1, (0,255,0), 2,8)
	
	l= len(contours)
	start_area = 0
	if l>0:
		index = 0
		#print "found orange"
		for i in range(l):
			area = cv2.contourArea(contours[i])
			if (area > start_area):  
				biggest_contour = cv2.contourArea(contours[i])
				start_area = area
				index = i
		cnt = contours[index]
		(x,y),radius = cv2.minEnclosingCircle(cnt)
		center = (int(x),int(y))
		radius = int(radius)
		img = cv2.circle(color_frame,center,  radius, (0,255,0),2,8)
	
	#gray_contour= cv2.drawContours(hsv_frame, contours, 3, (0,255,0),3)
	#cv2.imshow('contour',gray_contour)	
	cv2.imshow("cunt",color_frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
	 break

cap.release()
out.release()
cv2.destroyAllWindows





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


