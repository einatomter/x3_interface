# ssh -o "UserKnownHostsFile=/dev/null" -o 'StrictHostKeyChecking=no' root@192.168.1.101


import rospy
from p2_drone.msg import ImuData
import struct
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

mutex = threading.Lock()
imu_queue = list()

def subscribe_callback(data):
    mutex.acquire(blocking=True)

    # timestamp
    time = rospy.Time.now()

    imu_queue.append({time, data})

    mutex.release()


def publish_callback(event):
    mutex.acquire(blocking=True)

    if len(imu_queue) <= 0:
        return

    try:
        print(imu_queue[0])
        imu_queue.pop(0)

    except:
        pass

    # packed = struct.pack("6d2i",
    #                      data.accelerometer.x, data.accelerometer.y, data.accelerometer.z,
    #                      data.gyro.x, data.gyro.y, data.gyro.z,
    #                      time.secs, time.nsecs)
    # server.sendto(packed, ('192.168.1.255', 5678))

    mutex.release()

    
if __name__ == "__main__":
    rospy.init_node('node_name')
    rospy.Subscriber("/observer/calibrated_imu_data", ImuData, subscribe_callback)

    rospy.Timer(rospy.Duration(0.01), publish_callback)
    rospy.spin()

