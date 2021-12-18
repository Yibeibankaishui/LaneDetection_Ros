#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys
import time

import cv2
import numpy
import rospy
import sensor_msgs.msg
from cv_bridge import CvBridge, CvBridgeError, getCvType



QUEUE_SIZE = 10

# Send each image by iterate it from given array of files names  to a given topic,
# as a regular and compressed ROS Images msgs.
class Source:

    def __init__(self, topic, cam):
        self.pub = rospy.Publisher(topic, sensor_msgs.msg.Image, queue_size=QUEUE_SIZE)
        self.cap = cv2.VideoCapture(int(cam))

    def spin(self):
        cvb = CvBridge()
        while not rospy.core.is_shutdown():
            # 读视频
            ret, cvim = self.cap.read()
            # print(ret)
            # cvim = cv2.imread('/home/zhangcaocao/catkin_ws/src/lane_detection/test/test2.jpg')
            # 读入图像并裁剪
            # 相机读入尺寸为(480, 640)，原先为60，80
            cvim = cv2.resize(cvim ,(480, 640), interpolation=cv2.INTER_CUBIC)
            rate = rospy.Rate(30)
            rospy.loginfo("image shape: " + str(cvim.shape))
            # 发布图片消息，cv -> ros_img
            self.pub.publish(cvb.cv2_to_imgmsg(cvim))
            rate.sleep()

def main(args):
    s = Source('Image', args[1])
    rospy.init_node('Source')
    
    try:
        s.spin()
        rospy.spin()
        outcome = 'test completed'
    except KeyboardInterrupt:
        print ("shutting down")
        outcome = 'keyboard interrupt'
    rospy.core.signal_shutdown(outcome)

if __name__ == '__main__':
    # argv定义摄像头编号
    main(sys.argv)
