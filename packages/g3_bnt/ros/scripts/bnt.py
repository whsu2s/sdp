#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import tf
from math import radians, degrees


def sender():
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.init_node('input_test')
    file_name = rospy.get_param("bnt/goals_file")
    file = open(file_name,"r")
    #print file
    file_list =  file.readlines()
    database = dict()

    for i in file_list:
    	temp = [s.strip() for s in i.split(' ')]
    	key = temp[0]
    	value = [float(s) for s in temp[1:4]]
    	database[key] = value
    
    print "list of workspaces \n " +str(database)	

    # rate = rospy.Rate(10)
    pos = PoseStamped()

    while not rospy.is_shutdown():
        loc = raw_input()
	if (loc in database):
	    rospy.loginfo("workspace entered :" + str(loc))
		
	    value = database[loc]
	    # Euler to quaternion
	    q = tf.transformations.quaternion_from_euler(0, 0, value[2])
	    pos.pose.position.x = value[0]
	    pos.pose.position.y = value[1]
	    pos.pose.orientation.z = q[2]
	    pos.pose.orientation.w = q[3]
	    pos.header.frame_id = 'map'	
	    rospy.loginfo('goal sent')
	    rospy.loginfo('goal is being executed')
	    pub.publish(pos)
    # #     # rate.sleep()
	else:
	    print "please enter valid workspace"

if __name__ == '__main__':
    sender()
    
    

    
        
