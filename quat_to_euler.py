import rospy
import numpy as np
import math

#double check import statements
#rostopic info /imu/raw
from sensor_msgs import Imu
from geometry_msgs import Vector3

eulerPub = rospy.Publisher('imu/euler', Vector3, queue_size=200)

def quat_to_euler(imuMsg):
    x = imuMsg.orientation.x
    y = imuMsg.orientation.y
    z = imuMsg.orientation.z
    w = imuMsg.orientation.w

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.degrees(math.atan2(t3, t4))

    return roll, pitch, yaw

#callback function
def callback(imuMsg):
    ''' Convert imuMsg quaternions to euler angles and publish to imu/euler.
    '''

    #do the conversion
    roll, pitch, yaw = quat_to_euler(imuMsg)

    #init a new message
    msg = Vector3()
    msg.x = roll
    msg.y = pitch
    msg.z = yaw

    #publish the new message
    eulerPub.Publish(msg)

def listener():
    ''' Initialize node, subscribe to imu/raw, and run callback.
    '''

    #init the node
    rospy.init_node('quat_to_euler', anonymous=True)

    rospy.Subscriber('imu/raw', Imu, callback)

    rospy.spin()

if __name__ == '__main__':

    listener()
