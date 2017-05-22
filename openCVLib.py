import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2_objectDetect
from time import ctime



def color_filter(hsv_frame, color):

	if (color == 'blue'):
		lower_blue = np.array([110,50,50])
		upper_blue = np.array([130,255,255])
	if (color == 'orange'):
		lower_orange = np.array([0,150,210])
		upper_orange = np.array([44,291,286])
	if (color == 'red'):
		lower_orange = np.array([150,150,50])
		upper_orange = np.array([180,255,150])	
	
	"""
	#creating a mask to filter only orange, if any pixel falls in the range, it will be white
	#And this mask basically can be used for all purposes. It is 0 or 255 image with white 
	#as anywhere it matched the color window"""
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
	"""
	return mask


def smooth(frame_to_smooth, size_erode, size_dilate):
	kernel_erode = np.ones((size_erode,size_erode),np.uint8)
	kernel_dilate = np.ones((size_dilate,size_dilate),np.uint8)
	kernel = np.ones((15,15),np.float32)/225
	
	"""
	#below are different ways to blur. Median blur seems to be the best
	
	smoothed = cv2.filter2D(gray_frame, -1, kernel)
	cv2.imshow('smooth',smoothed)
	blur = cv2.GaussianBlur(gray_frame, (15,15), 0)
	cv2.imshow('blur',blur)
	
	median = cv2.medianBlur(gray_frame, 15)
	cv2.imshow('median',median)
	"""
	
	"""eroding the edges to smoothen the pictures by eroding the boundaries, 
	use the kernel to do this """
	erosion = cv2.erode(frame_to_smooth, kernel_erode, iterations =1)
	
	"""
	#expand the pixels inside the orange object that I want to track
	#used because sometimes there are holes inside a full object. this will make it whole"""
	smoothed_frame= cv2.dilate(erosion, kernel_dilate, iterations =1)
	#cv2.imshow('dilation',smoothed_frame)	
	
	"""
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	#cv2.imshow('open',opening) #removes false negative. removes white in the background
	cv2.imshow('close',closing) #removes false positives. removes holes within the object

	closing = closing.copy()
	"""
		
	return smoothed_frame


def draw_contour(frame, contours, contour_type):
		x_center = -1
		y_center = -1
		
		l= len(contours)
		start_area = 0
		if l>0:
			#print "found orange"
			for i in range(l):
				area = cv2.contourArea(contours[i])
				if (area > start_area):  
					biggest_contour = cv2.contourArea(contours[i])
					start_area = area
					index = i
			cnt = contours[index]
			
			if contour_type == 'circle':
				(x,y),radius = cv2.minEnclosingCircle(cnt)
				center = (int(x),int(y))
				radius = int(radius)
				img = cv2.circle(frame,center,radius, (0,255,0),2,8)

			elif contour_type == 'poly':
				peri = cv2.arcLength(cnt, True)
				rect = cv2.approxPolyDP(cnt, 0.1 * peri, True) 
				cv2.drawContours(frame, [rect], -1, (0,255,0), 2,8)
			
			elif contour_type == 'rect':
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2,8)	
			
			elif contour_type == 'ellipse':
				ellipse = cv2.fitEllipse(cnt)
				img = cv2.ellipse(frame, ellipse, (0,255,0),2)
				
			elif contour_type == 'none':
				cv2.drawContours(frame, contours, -1, (0,255,0), 2,8)
				
			leftmost = tuple(cnt[cnt[:,:,0].argmin()][0]) 
			rightmost = tuple(cnt[cnt[:,:,0].argmax()][0]) 
			topmost = tuple(cnt[cnt[:,:,1].argmin()][0]) 
			bottomtmost = tuple(cnt[cnt[:,:,1].argmax()][0]) 	
			x_center = (leftmost[0]+rightmost[0])/2
			y_center = (topmost[1]+bottomtmost[1])/2
			
			
		return frame, x_center, y_center
	
def write_frame(frame, string, date, color):
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, string, (120,40), font, 0.5 , color, 2)
	cv2.putText(frame, date, (0,470), font, 0.5 , (0,0,0), 2)
	return frame
	

	
def discard_t_sec(cap,t): #not using the first 10 sec as the camera does some focussing 
	i =0
	index = 20*t #frames/sec * time
	while i in range(index):
		ret , frame = cap.read()
		#cv2.imshow('frame',frame)
		i = i+1 
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


"""
detecting difference between two consective images 
if the pixel difference is less than 20, then force them to 0, so that 
cv2.countNonZero(diff) will not false trigger. if pixel difference is greater than 
10, must be a real movement and then force them to 255.255 is black and 0 will appear as white
"""
def diffImg(t0,t1,t2):
	ret, ThreshImage = cv2.threshold(cv2.absdiff(t2,t1), 10 ,255, cv2.THRESH_BINARY)
	#cv2.imshow('diffimage',cv2.absdiff(t2,t1)) # this is the grey image difference
	#cv2.imshow('threshimage',ThreshImage) 
	#ThreshImage = cv2.GaussianBlur(ThreshImage, (5,5),0)
	smooth_image = smooth(ThreshImage, 5, 5)
	#cv2.imshow('smoothImage',smooth_image)
	return smooth_image




	

