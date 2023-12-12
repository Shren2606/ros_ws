#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist


import imutils
import cv2

counter = 0
def image_callback(msg):

    try:
        bridge = CvBridge()
        twist_msg = Twist()
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        

        template = cv2.imread('/home/nhathai/ros_ws/data/frame_template.jpg')
        template = imutils.resize(template, width=100)

        #image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)# xoay ảnh 90*
        image = imutils.resize(image, width=300,height=300)# resize ảnh

        height, width, _ = image.shape
        part_width = width // 3
        cv2.line(image, (1 * part_width, 0), (1 * part_width, height), (255, 0, 0), 2)
        cv2.line(image, (2 * part_width, 0), (2* part_width, height), (255, 0, 0), 2)

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc  = cv2.minMaxLoc(result)
        w, h = template.shape[1], template.shape[0]
        top_left = max_loc
        if max_val > 0.6:
            bottom_right = (top_left[0] + w, top_left[1] + h)
            tâm_x = (top_left[0] + bottom_right[0]) // 2
            tâm_y = (top_left[1] + bottom_right[1]) // 2
            setpoint = 150
            angular=(tâm_x-setpoint)*150/300*0.5
            # Vẽ hộp giới hạn xung quanh vật
            
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.circle(image, (tâm_x, tâm_y), 5, (255, 255, 0), -1)
        else:
            angular = 0

        twist_msg.linear.x = 0  # Replace 0.1 with your desired linear velocity
        twist_msg.angular.z = angular  # Replace 0.2 with your desired angular velocity

        # Publish the Twist message
        pub.publish(twist_msg)

        # Chuyển đổi frame sang định dạng ROS Image
        ros_image = bridge.cv2_to_imgmsg(image, encoding="bgr8")

        # Publish frame lên topic
        pub_img.publish(ros_image)

        rospy.loginfo(f'Follow person!, max_val: {max_val}')


    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        rospy.init_node('follow_person', anonymous=True)
        pub_img = rospy.Publisher('/cv_camera/image_detec', Image, queue_size=1)
        pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/cv_camera/image_raw", Image, callback=image_callback)
        
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
