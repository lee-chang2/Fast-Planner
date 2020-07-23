#!/usr/bin/env python3

import rospy
import math
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Pose
from tf.tranformations import *


class CameraRotate:

    NODE_NAME="camera_rotate"
    ODOMETRY_TOPIC="odom"
    CAMERA_POSE_TOPIC="camera_pose"
    QUEUE_SIZE=10
    RATE_HZ=10
    #ROTATION_RPY = [0, 0, math.pi/2]
    P = math.pi/2
    ROTATION_RPY = [-P, 0, -P]

    def __init__(self):
        rospy.init_node(self.NODE_NAME, anonympus=False)
        self.sub = rospy.Subscriber(self.ODOMETRY_TOPIC, Odometry, self.transform)
        self.pub = rospy.Publisher(self.CAMERA_POSE_TOPIC, PoseStamped, queue_size=self.QUEUE_SIZE)
        self.rot_quat = quaternion_from_euler(self.ROTATION_RPY[0], self.ROTATION_RPY[1], self.ROTATION_RPY[2])
        self.pub_rate = rospy.Rate(self.RATE_HZ)
        rospy.loginfo("<<Camera Pose Rotation>>: node: %s, input_topic: /%s, output_topic: /%s" % \
                      self.NODE_NAME, self.ODOMETRY_TOPIC, self.CAMERA_POSE_TOPIC)

    def transform(self, msg):
        orientation = msg.pose.pose.orientation
        odom_quat = [orientation.x, orientation.y, orientation.z, orientation.w]
        rotated = self.quaternion_rotation(self.rot_quat, odom_quat)

        orientation_msg = Quaternion(rotated[0], rotated[1], rotated[2], rotated[3])
        position_msg = Pose(position=msg.pose.pose.position, orientation=orientation_msg)
        camera_pose_msg = PoseStamped(header=msg.header, pose=position_msg)

        self.pub.publish(camera_pose_msg)

        @staticmethod
        def quaternion_rotation(rot_quat, quat):
            quat_mul = quaternion_multiply(rot_quat, quat)
            return quat_mul / np.linalg.norm(quat_mul)

if __name__ == '__main__':
    try:
        camera_rotate = CameraRotate()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
    