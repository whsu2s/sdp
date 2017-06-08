#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

def sender():
    pub = rospy.Publisher('loc', PoseStamped, queue_size=10)
    rospy.init_node('input_test')
    rate = rospy.Rate(10)
    pos = PoseStamped()

    while not rospy.is_shutdown():
        loc = raw_input()
        if loc == 'pos0':
            pos.pose.position.x = 0.0
            pos.pose.position.y = 0.0
            pos.pose.orientation.z = 0
        elif loc == 'pos1':
            pos.pose.position.x = 0.0
            pos.pose.position.y = 10.0
            pos.pose.orientation.z = 0.5
        elif loc == 'pos2':
            pos.pose.position.x = 10.0
            pos.pose.position.y = 5.0
            pos.pose.orientation.z = 0.5

        rospy.loginfo('pose')
        pub.publish(pos)
        rate.sleep

if __name__ == '__main__':
    sender()
    
    

    
        
