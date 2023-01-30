#!/usr/bin/env python3

import os
import threading
import rospy
from sensor_msgs.msg import Imu
from x3_interface.msg import ImuData

mutex = threading.Lock()
imu_queue = list()

def subscribe_callback(data: ImuData):

    mutex.acquire(blocking=True)

    imu_queue.append(data)

    mutex.release()

def publish_callback(event):

    mutex.acquire(blocking=True)

    imu_out = Imu()

    try:

        # header
        imu_out.header.frame_id = 'imu0'
        imu_out.header.stamp = rospy.Time.now()

        # orientation
        imu_out.orientation.w = 1
        imu_out.orientation.x = 0
        imu_out.orientation.y = 0
        imu_out.orientation.z = 0

        for index in imu_out.orientation_covariance:
            index = 0

        # angular velocity
        imu_out.angular_velocity.x = imu_queue[0].gyro.x
        imu_out.angular_velocity.y = imu_queue[0].gyro.y
        imu_out.angular_velocity.z = imu_queue[0].gyro.z

        for index in imu_out.angular_velocity_covariance:
            index = 0

        # linear acceleration
        imu_out.linear_acceleration.x = imu_queue[0].accelerometer.x * 10
        imu_out.linear_acceleration.y = imu_queue[0].accelerometer.y * 10
        imu_out.linear_acceleration.z = imu_queue[0].accelerometer.z * 10

        for index in imu_out.linear_acceleration_covariance:
            index = 0

        imu_queue.pop(0)

        # publish
        output_pub.publish(imu_out)
    
    except:
        pass

    mutex.release()


if __name__ == '__main__':

    # Start the node
    node_name = os.path.splitext(os.path.basename(__file__))[0]
    rospy.init_node(node_name)
    rospy.loginfo('Starting [%s] node' % node_name)

    output_pub = rospy.Publisher('/x3/imu', Imu, queue_size=1)
    # first_publish = rospy.wait_for_message('/custom_observer/imu_timestamped', Imu)

    input_sub = rospy.Subscriber('/observer/calibrated_imu_data', ImuData, subscribe_callback)

    # initial delay
    rospy.sleep(0.4)

    rospy.Timer(rospy.Duration(0.01), publish_callback)

    # Ros Spin
    rospy.spin()

    rospy.loginfo('Shutting down [%s] node' % node_name)
