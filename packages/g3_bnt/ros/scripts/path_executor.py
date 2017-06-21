#!/usr/bin/env python

PACKAGE = 'g3_bnt'

import roslib
roslib.load_manifest(PACKAGE)
import rospy
import tf
import actionlib
from actionlib import SimpleActionClient, SimpleActionServer
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback, MoveBaseActionResult,MoveBaseAction
#from actionlib.msg import GoalID, GoalStatusArray
from std_srvs.srv import Empty
class PathExecutor:
    
    def __init__(self):

	self._feedback = MoveBaseActionFeedback() 
	self._result = MoveBaseActionResult()
        self._ep_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        while True:
	    goals = self.get_user_input()
	    print goals
            self.execute(goals)
    def get_user_input(self):
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


		#while not rospy.is_shutdown():
		    
						
        loc = raw_input()
    
        workspace = [s.strip() for s in loc.split(' ')]
	
	goal_sequence = []
        print workspace[0]
	print workspace[1]				#	rospy.loginfo("workspace entered :" + str(loc))
	for ws in workspace:
	    value = database[ws]
		# Euler to quaternion
	    action_goal = MoveBaseActionGoal()
	    q = tf.transformations.quaternion_from_euler(0, 0, value[2])
	    action_goal.goal.target_pose.pose.position.x = value[0]
	    action_goal.goal.target_pose.pose.position.y = value[1]
	    action_goal.goal.target_pose.pose.orientation.x = q[0]
	    action_goal.goal.target_pose.pose.orientation.y = q[1]
	    action_goal.goal.target_pose.pose.orientation.z = q[2]
	    action_goal.goal.target_pose.pose.orientation.w = q[3]
	    action_goal.goal.target_pose.header.frame_id = 'map'
	    goal_sequence.append(action_goal.goal)

			#else:
			#	print "please enter valid workspace"
	return goal_sequence 
    def execute(self, goal_sequence):
	rospy.wait_for_service('/move_base/clear_costmaps')
	cc = rospy.ServiceProxy('/move_base/clear_costmaps',Empty)
        success = True
        rospy.loginfo('Received goal.')
        for current_pose in (goal_sequence):
            # check that preempt has not been requested by the client
            
            self._ep_client.wait_for_server()
	    cc()
            self._ep_client.send_goal(current_pose)
	   # try:
					   
	#	cc() 
	 #   except rospy.ServiceException, e:
	  #      print "Service call failed: %s"%e
	    rospy.loginfo('goal sent')
	    rospy.loginfo('goal is being executed')
            self._ep_client.wait_for_result()


            state = self._ep_client.get_state()
            if state == 3:
                rospy.loginfo("succeeded")


if __name__ == '__main__':
    rospy.init_node('path_execute')
    path = PathExecutor()
    rospy.spin()
