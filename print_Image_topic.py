#!/usr/bin/env python

import rospy
#from std_msgs.msg import Int32
from sensor_msgs.msg import Image

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.data)
    rows = data.height
    cols = data.width
    img = data.encoding
    print("Image matrix of size " + str(rows) + " " + str(cols) + ": " + img)
    #print ("Image matrix of size " + str(rows) + " " + str(cols))

def listener():
    rospy.init_node('listener', anonymous = True)
    rospy.Subscriber("/two_wheels_robot/camera1/image_raw", Image, callback)
    rospy.spin()
    
if __name__ == '__main__':
    listener()
