#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import numpy as np
from io import StringIO

def sender():
    pub = rospy.Publisher('loc', PoseStamped, queue_size=10)
    rospy.init_node('input_test')
    file = open("goal.txt","r")
    #print file
    file_list =  file.readlines()
    database = dict()

    for i in file_list:
    	temp = [s.strip() for s in i.split(' ')]
    	key = temp[0]
    	value = [float(s) for s in temp[1:4]]
    	database[key] = value
    print database	

    # rate = rospy.Rate(10)
    pos = PoseStamped()

    while not rospy.is_shutdown():
        loc = raw_input()
        value = database[loc]
        pos.pose.position.x = value[0]
        pos.pose.position.y = value[1]
        pos.pose.orientation.z = value[2]
        

        rospy.loginfo('goal sent')
        pub.publish(pos)
    # #     # rate.sleep()

if __name__ == '__main__':
    sender()
    
    

    
        
