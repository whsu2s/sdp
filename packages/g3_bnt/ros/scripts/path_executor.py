#!/usr/bin/env python

PACKAGE = 'g3_bnt'

import roslib
roslib.load_manifest(PACKAGE)
import rospy

from actionlib import SimpleActionClient, SimpleActionServer
from move_base.msgs import MoveBaseActionGoal, MoveBaseActionFeedback, MoveBaseActionResult,MoveBaseAction
from actionlib.msgs import GoalID, GoalStatusArray

class PathExecutor:
    
    def __init__(self):

		self._feedback = MoveBaseActionFeedback() 
		self._result = MoveBaseActionResult()
		self.action_goal = MoveBaseActionGoal()
		self.goal_sequence = []
		self.get_user_input()
        #use path_executor as server for the terminal client
        self._as = SimpleActionServer('move_base/goal',MoveBaseAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        #rospy.loginfo('Started path_executor.')

        self._ep_client = actionlib.SimpleActionClient('move_base/goal', MoveBaseActionGoal)
        
    
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
			#if (for loc in database):
			#	rospy.loginfo("workspace entered :" + str(loc))
		for l in loc:
			value = database[l]
			# Euler to quaternion
			q = tf.transformations.quaternion_from_euler(0, 0, value[2])
			self.action_goal.goal.pose.position.x = value[0]
			self.action_goal.goal.pose.position.y = value[1]
			self.action_goal.goal.pose.orientation.x = q[0]
			self.action_goal.goal.pose.orientation.y = q[1]
			self.action_goal.goal.pose.orientation.z = q[2]
			self.action_goal.goal.pose.orientation.w = q[3]
			self.action_goal.goal.header.frame_id = 'map'
			self.goal_sequence.append(action_goal.goal)

			#else:
			#	print "please enter valid workspace"

    def execute_cb(self, goal_sequence):
		rospy.wait_for_service('/move_base/clear_costmaps')
		cc = rospy.ServiceProxy('/move_base/clear_costmaps',Empty)
        success = True
        rospy.loginfo('Received goal.')
        for current_pose in (goal_sequence):
            # check that preempt has not been requested by the client
            
            current_goal = self.action_goal

            current_goal.goal = current_pose
            self._ep_client.wait_for_server()
            self._ep_client.send_goal(current_goal)
			try:
					   
						cc() 
					except rospy.ServiceException, e:
						print "Service call failed: %s"%e
			rospy.loginfo('goal sent')
			rospy.loginfo('goal is being executed')
            self._ep_client.wait_for_result()

            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted')
                self._as.set_preempted()
           
                break


            state = self._ep_client.get_state()
            if state == 3:
                rospy.loginfo("succeeded")


        #let terminal client know the result
        if success:
            self._as.set_succeeded(self._result)
        




if __name__ == '__main__':
    rospy.init_node()
    PathExecutor()
    rospy.spin()
