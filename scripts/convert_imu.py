#!/usr/bin/env python3

import os
import rospy
from sensor_msgs.msg import Imu
from x3_interface.msg import ImuData

GRAVITY_CONSTANT = 9.81

def subscribe_callback(data: ImuData):

    imu_out = Imu()

    # header
    imu_out.header.frame_id = 'imu0'
    imu_out.header.stamp = rospy.get_rostime()# + rospy.Duration.from_sec(0.270)


    # orientation
    imu_out.orientation.w = 1
    imu_out.orientation.x = 0
    imu_out.orientation.y = 0
    imu_out.orientation.z = 0

    for index in imu_out.orientation_covariance:
        index = 0

    # angular velocity
    imu_out.angular_velocity.x = data.gyro.x# * 1.5
    imu_out.angular_velocity.y = data.gyro.y# * 1.5
    imu_out.angular_velocity.z = data.gyro.z# * 1.5

    for index in imu_out.angular_velocity_covariance:
        index = 0

    # linear acceleration
    imu_out.linear_acceleration.x = data.accelerometer.x * GRAVITY_CONSTANT
    imu_out.linear_acceleration.y = data.accelerometer.y * GRAVITY_CONSTANT
    imu_out.linear_acceleration.z = data.accelerometer.z * GRAVITY_CONSTANT

    for index in imu_out.linear_acceleration_covariance:
        index = 0

    # publish
    output_pub.publish(imu_out)



if __name__ == '__main__':

    # Start the node
    # node_name = os.path.splitext(os.path.basename(__file__))[0]
    node_name = 'convert_imu'
    rospy.init_node(node_name)
    rospy.loginfo('Starting [%s] node' % node_name)

    output_pub = rospy.Publisher('/x3/imu', Imu, queue_size=1)
    # first_publish = rospy.wait_for_message('/custom_observer/imu_timestamped', Imu)

    input_sub = rospy.Subscriber('/observer/calibrated_imu_data', ImuData, subscribe_callback)

    # Ros Spin
    rospy.spin()

    rospy.loginfo('Shutting down [%s] node' % node_name)
