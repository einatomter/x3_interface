#!/usr/bin/env python3

# Keyboard teleop for the x3 rover
# Code uses uuv teleop as reference

from __future__ import print_function
import os
import time
import sys, termios
import rospy
from sensor_msgs.msg import FluidPressure

from blueye.sdk import Drone


def callback(drone: Drone):
    
    print(f"depth: {drone.depth} mm")

    depth = FluidPressure()
    # depth.header = rospy.Header()
    depth.header.frame_id = "depth"
    # depth.header.stamp = rospy.get_rostime()
    # depth.fluid_pressure = drone.depth/1000
    # output_pub.publish(depth)

if __name__ == '__main__':

    # Start the node
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)
    rospy.loginfo('Starting [%s] node' % node_name)

    myDrone = Drone(slaveModeEnabled=True)
    print("Fetch depth: drone connected!")
    output_pub = rospy.Publisher('x3/depth', FluidPressure, queue_size=1)

    # Ros Spin
    # rate = rospy.Rate(50) # Hz
    while not rospy.is_shutdown():
        time.sleep(0.2)
        callback(myDrone)

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    rospy.loginfo('Shutting down [%s] node' % node_name)
