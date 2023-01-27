# ssh -o "UserKnownHostsFile=/dev/null" -o 'StrictHostKeyChecking=no' root@192.168.1.101
# export ROS_MASTER_URI=http://192.168.1.101:11311

import rospy
from sensor_msgs.msg import Imu
from p2_drone.msg import ImuData

def subscribe_callback(data):

    imu_out = Imu()
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
    imu_out.angular_velocity.x = data.gyro.x
    imu_out.angular_velocity.y = data.gyro.y
    imu_out.angular_velocity.z = data.gyro.z

    for index in imu_out.angular_velocity_covariance:
        index = 0

    # linear acceleration
    imu_out.linear_acceleration.x = data.accelerometer.x * 10
    imu_out.linear_acceleration.y = data.accelerometer.y * 10
    imu_out.linear_acceleration.z = data.accelerometer.z * 10

    for index in imu_out.linear_acceleration_covariance:
        index = 0

    output_pub.publish(imu_out)
    
if __name__ == "__main__":
    rospy.init_node('node_name')
    rospy.Subscriber("/observer/calibrated_imu_data", ImuData, subscribe_callback)
    output_pub = rospy.Publisher('/custom_observer/imu_timestamped', Imu, queue_size=1)

    rospy.spin()

