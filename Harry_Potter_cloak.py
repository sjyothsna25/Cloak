import cv2
import numpy
#pip install opencv-python

#initial function for the callin of the trackbar
def justfunc(x):
	#only for referece
	print("")

#initialisation of the camera
capture = cv2.VideoCapture(0)
All_bars = cv2.namedWindow("All_bars")

cv2.createTrackbar("upper_hue","All_bars",110,180,justfunc)
cv2.createTrackbar("upper_saturation","All_bars",255, 255, justfunc)
cv2.createTrackbar("upper_value","All_bars",255, 255, justfunc)
cv2.createTrackbar("lower_hue","All_bars",68,180, justfunc)
cv2.createTrackbar("lower_saturation","All_bars",55, 255, justfunc)
cv2.createTrackbar("lower_value","All_bars",54, 255, justfunc)

#Capturing the initial frame for creation of background
while(True):
	cv2.waitKey(1000)
	ret,init_frame = capture.read()
	#check if the frame is returned then brake
	if(ret):
		break

# Start captureturing the frames for actual magic!!
while(True):
	ret,frame = capture.read()
	#The method cv2.cvtColor() transforms colorspace.
	bgrtohsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#getting the HSV values for masking the cloak
	upper_hue = cv2.getTrackbarPos("upper_hue", "All_bars")
	upper_saturation = cv2.getTrackbarPos("upper_saturation", "All_bars")
	upper_value = cv2.getTrackbarPos("upper_value", "All_bars")
	lower_value = cv2.getTrackbarPos("lower_value","All_bars")
	lower_hue = cv2.getTrackbarPos("lower_hue","All_bars")
	lower_saturation = cv2.getTrackbarPos("lower_saturation","All_bars")

	#Kernel to be used for dilation
	kernel = numpy.ones((3,3),numpy.uint8)

	upper_hsv = numpy.array([upper_hue,upper_saturation,upper_value])
	lower_hsv = numpy.array([lower_hue,lower_saturation,lower_value])

#The cv2.inRange() method returns a segmented binary mask of the frame containing the blue colour.
	# mask if blue shows white  else shows black
	mask = cv2.inRange(bgrtohsv, lower_hsv, upper_hsv)
	#Here, the central element of the image is replaced by the median of all the pixels in the kernel area. This operation processes the edges while removing the noise.
	mask = cv2.medianBlur(mask,3)
	mask_inverse = 255-mask 
	mask = cv2.dilate(mask,kernel,5)
	#mask= blue->white
	#mask_inverse=blue to black
	#The mixing of frames in a combination to achieve the required frame
	b = frame[:,:,0]
	g = frame[:,:,1]
	r = frame[:,:,2]
	b = cv2.bitwise_and(mask_inverse, b)
	g = cv2.bitwise_and(mask_inverse, g)
	r = cv2.bitwise_and(mask_inverse, r)
    #blanket frame+ (black cloack)
	#0*anything zero(black)
	frame_inv = cv2.merge((b,g,r))

	b = init_frame[:,:,0]
	g = init_frame[:,:,1]
	r = init_frame[:,:,2]
	b = cv2.bitwise_and(b,mask)
	g = cv2.bitwise_and(g,mask)
	r = cv2.bitwise_and(r,mask)
	#mask->blue->white*background=background
	blanket_area = cv2.merge((b,g,r))

	final = cv2.bitwise_or(frame_inv, blanket_area)

	cv2.imshow("Harry's Cloak",final)
	cv2.imshow("original image",frame)
	if(cv2.waitKey(3) == ord('q')):
		break;

cv2.destroyAllWindows()
capture.release()




