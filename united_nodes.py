#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

# Instantiate CvBridge
bridge = CvBridge()

class velPublisher:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        # Set up your subscriber and define its callback
        rospy.Subscriber("/two_wheels_robot/camera1/image_raw", Image, self.image_callback)
        rospy.Subscriber("/base_scan", LaserScan, self.lidar_callback)
        print ("Publishers ok")
        print ("Starting node...")

        self.velocity = Twist()
        self.anglemin = 0
        self.rangemin = 0
        self.ranges = []
        self.auxmin = 0
        self.signal = 2; # 0 -> MoveFoward; 1 -> stop; 2 -> TurnRight; 3 -> TurnLeft
        
        r = rospy.Rate(10) #10Hz
        print ("Node initialized to 10 Hz")
        
        while not rospy.is_shutdown():
            #print("Publishing...")
            if (self.rangemin < 0.8 and (self.anglemin > -20.0 and self.anglemin < 20.0 ) and self.signal == 2):                
                self.velocity.linear.x = 0.1 #[m/s]
                self.velocity.angular.z = 1.5 #[rad/s]
                time.sleep(1.5)           
            elif (self.rangemin < 0.8 and (self.anglemin > -20.0 and self.anglemin < 20.0 ) and self.signal == 1):
                self.velocity.linear.x = 0 #[m/s]
                self.velocity.angular.z = 0 #[rad/s]
            elif (self.rangemin < 0.8 and (self.anglemin > -20.0 and self.anglemin < 20.0 ) and self.signal == 3):
                self.velocity.linear.x = 0.1 #[m/s]
                self.velocity.angular.z = -1.5 #[rad/s]
                time.sleep(1.5)                
            else:            
                self.velocity.linear.x = 0.1 #[m/s]
                self.velocity.angular.z = 0 #[rad/s]                           
                        
            self.pub_cmd_vel.publish(self.velocity) #publish the number
            print(self.velocity)
            r.sleep()
            
    def image_callback(self, msg):
    #print("Received an image!")
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            cv2.imwrite('camera_image.jpeg', cv2_img)
    
    def lidar_callback (self, msg):
        self.ranges = msg.ranges
        self.rangemin= min(self.ranges)
        
        #this allow to select items-from the data-store by identifying a sigle value wich must match with the range and the angle
        self.auxmin = self.ranges.index(self.rangemin)
        
        #conversion from radians to degrees
        self.anglemin = (self.auxmin*msg.angle_increment * 180/3.1416) - 180
    
    def cleanup(self):
        #stop the robot before finishing a node
        print("Stop the robot before dying")
        self.velocity.angular.z = 0    
        self.velocity.linear.x = 0
        self.pub_cmd_vel.publish(self.velocity)

if __name__ == "__main__":
    rospy.init_node("cmd_vel_publisher", anonymous = True)
    try:
        velPublisher()
    except:
        rospy.logfatal("cmd_vel_publisher died")
