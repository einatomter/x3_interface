#!/usr/bin/env python3

import os
import rospy
from sensor_msgs.msg import FluidPressure
from std_msgs.msg import Float32

def subscribe_callback(data: Float32):

    depth_out = FluidPressure()

    # header
    depth_out.header.frame_id = 'depth0'
    depth_out.header.stamp = rospy.get_rostime()

    depth_out.fluid_pressure = data.data
    depth_out.variance = 0

    # publish
    output_pub.publish(depth_out)



if __name__ == '__main__':

    # Start the node
    # node_name = os.path.splitext(os.path.basename(__file__))[0]
    node_name = 'convert_depth'
    rospy.init_node(node_name)
    rospy.loginfo('Starting [%s] node' % node_name)

    output_pub = rospy.Publisher('/x3/depth', FluidPressure, queue_size=1)
    # first_publish = rospy.wait_for_message('/custom_observer/imu_timestamped', Imu)

    input_sub = rospy.Subscriber('/sensor_depth/depth', Float32, subscribe_callback)

    # Ros Spin
    rospy.spin()

    rospy.loginfo('Shutting down [%s] node' % node_name)
