#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import tf
import roslib
roslib.load_manifest('g3_bnt')
import rospy
import actionlib
 
from move_base.msgs import MoveBaseActionGoal, MoveBaseActionFeedback, MoveBaseActionResult
from actionlib.msgs import GoalID, GoalStatusArray
from std_srvs.srv import Empty

def sender():
    #pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.init_node('input_test')
	
	client = actionlib.SimpleActionClient('move_base/goal', MoveBaseActionGoal)
    client.wait_for_server()


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

    
    rospy.wait_for_service('/move_base/clear_costmaps')
    cc = rospy.ServiceProxy('/move_base/clear_costmaps',Empty)
    while not rospy.is_shutdown():
        
		goal = MoveBaseGoal(order=15)

        loc = raw_input()
		if (loc in database):
			rospy.loginfo("workspace entered :" + str(loc))
			for l in loc:
				value = database[l]
				# Euler to quaternion
				q = tf.transformations.quaternion_from_euler(0, 0, value[2])
				goal.pose.position.x = value[0]
				goal.pose.position.y = value[1]
			    goal.pose.orientation.x = q[0]
			    goal.pose.orientation.y = q[1]
				goal.pose.orientation.z = q[2]
				goal.pose.orientation.w = q[3]
				goal.header.frame_id = 'map'
				client.send_goal(goal)
				try:
				   
				    cc() 
				except rospy.ServiceException, e:
				    print "Service call failed: %s"%e
				rospy.loginfo('goal sent')
				rospy.loginfo('goal is being executed')
    			client.wait_for_result(rospy.Duration.from_sec(5.0))	
				client.get_result()
				rospy.loginfo('goal is finished')
				#pub.publish(pos)
				
				
		else:
	    	print "please enter valid workspace"

if __name__ == '__main__':
    sender()
    

        
