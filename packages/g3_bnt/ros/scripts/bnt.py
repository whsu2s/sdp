#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import tf
from math import radians, degrees
from std_srvs.srv import Empty

def sender():
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.init_node('input_test')
    file_name = rospy.get_param("bnt/goals_file")
    file = open(file_name,"r")
    file_list =  file.readlines()
    database = dict()

    for i in file_list:
	# 
    	temp = [s.strip() for s in i.split(' ')]
    	key = temp[0]
	# convert to float
    	value = [float(s) for s in temp[1:4]]
    	database[key] = value
    
    print "list of workspaces \n " +str(database)	

    pos = PoseStamped()
    rospy.wait_for_service('/move_base/clear_costmaps')
    cc = rospy.ServiceProxy('/move_base/clear_costmaps',Empty)
    while not rospy.is_shutdown():
        try:
           
            cc() 
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

        loc = raw_input()
	if (loc in database):
	    rospy.loginfo("workspace entered :" + str(loc))
		
	    value = database[loc]
	    # Euler to quaternion
	    q = tf.transformations.quaternion_from_euler(0, 0, value[2])
	    pos.pose.position.x = value[0]
	    pos.pose.position.y = value[1]
            pos.pose.orientation.x = q[0]
            pos.pose.orientation.y = q[1]
	    pos.pose.orientation.z = q[2]
	    pos.pose.orientation.w = q[3]
	    pos.header.frame_id = 'map'	
	    rospy.loginfo('goal sent')
	    rospy.loginfo('goal is being executed')
	    pub.publish(pos)
	else:
	    print "please enter valid workspace"

if __name__ == '__main__':
    sender()
    
    

    
        
