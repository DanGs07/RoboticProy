# !/usr/bin/env python 
import rospy
import cv2
from sensor_msgs.msg import Image, String
from cv_bridge import CvBridge, CVBridgeError
bridge = CvBridge()
cv image = bridge.imgmsg_to_cv2(image_message, dessired_encoding='passthrough')

#################################################################################################
#												#
# PSEUDOCODE											#
# 1. Read image from the robotcamera								#
# 2. Convert ROS image into a OpenCv image							#
# 3. Convert image type (IF NEEDED) into an RGB image to easy manipulation                      #
# 4. Evaluate the needed colors on the image                             			#
# 5. Evaluate conditions depending on the colors readed on the image				#
#												#
#################################################################################################}

class img_conv:
	##### SUBSCRIBERS #####
	self.imgSub = rospy
