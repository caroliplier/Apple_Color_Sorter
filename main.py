# Python code for Multiple Color Detection 

import paho.mqtt.client as mqtt
import numpy as np 
import cv2 

run_once_flag = True

contourRed = 0
contourGreen = 0

# MQTT broker details
# broker_address = "192.168.222.178"  # Replace with your MQTT broker's address
broker_address = "192.168.43.178"  # Replace with your MQTT broker's address
port = 1883  # Default MQTT port

# Callback function for when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")


# Create an MQTT client
client = mqtt.Client()  # Using userdata to store state

# Set the callback function for when the client connects to the broker
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker_address, port)

# Run the MQTT client loop in the background
client.loop_start()

# Function to publish a message to a topic
def publish_to_topic(topic, message):
    client.publish(topic, message)
    print(f"Published: {message} to topic: {topic}")

# Capturing video through webcam 
webcam = cv2.VideoCapture(2) 
  
# Start a while loop 
while(1): 
	
	# Reading the video from the 
	# webcam in image frames 
	_, imageFrame = webcam.read() 

	# Convert the imageFrame in 
	# BGR(RGB color space) to 
	# HSV(hue-saturation-value) 
	# color space 
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

	# Set range for red color and 
	# define mask 
	red_lower = np.array([136, 87, 111], np.uint8) 
	red_upper = np.array([180, 255, 255], np.uint8) 
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

	# Set range for green color and 
	# define mask 
	green_lower = np.array([25, 52, 72], np.uint8) 
	green_upper = np.array([102, 255, 255], np.uint8) 
	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between imageFrame and mask determines 
	# to detect only that particular color 
	kernel = np.ones((5, 5), "uint8") 
	
	# For red color 
	red_mask = cv2.dilate(red_mask, kernel) 
	res_red = cv2.bitwise_and(imageFrame, imageFrame, 
							mask = red_mask) 
	
	# For green color 
	green_mask = cv2.dilate(green_mask, kernel) 
	res_green = cv2.bitwise_and(imageFrame, imageFrame, 
								mask = green_mask) 
	

	# Creating contour to track red color 
	contours, hierarchy = cv2.findContours(red_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		contourRed = area
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 0, 255), 2) #Red Rectangle
			
			cv2.putText(imageFrame, "Red Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
						(0, 0, 255))	
			if run_once_flag:
				topic = "iloveapple"  # Replace with the desired MQTT topic
				message = "red"
				publish_to_topic(topic, message)
				run_once_flag = False

	# Creating contour to track green color 
	contours, hierarchy = cv2.findContours(green_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
	
	for pic, contour in enumerate(contours): 
		area = cv2.contourArea(contour) 
		contourGreen = area
		if(area > 300): 
			x, y, w, h = cv2.boundingRect(contour) 
			imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 255, 0), 2) 
			
			cv2.putText(imageFrame, "Green Colour", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						1.0, (0, 255, 0)) 
			if run_once_flag:
				topic = "iloveapple"  # Replace with the desired MQTT topic
				message = "green"
				publish_to_topic(topic, message) 
				run_once_flag = False
	prevcontourGreen = contourGreen
	prevcontourRed = contourRed
		
	if (contourGreen < 2) and (contourRed < 2 ) :
		run_once_flag = True
	if contourGreen == prevcontourGreen:
		contourGreen =0
	if contourRed == prevcontourRed:
		contourRed =0
	print(run_once_flag)
	print(contourGreen)
	print(contourRed)
	

	# Program Termination 
	cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		cap.release() 
		cv2.destroyAllWindows() 
		break
