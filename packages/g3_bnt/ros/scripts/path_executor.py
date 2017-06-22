#!/usr/bin/env python

PACKAGE = 'g3_bnt'

import roslib
roslib.load_manifest(PACKAGE)
import rospy
import tf
import actionlib
from actionlib import SimpleActionClient
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from std_srvs.srv import Empty

class Position:
	def __init__(self,x,y):

		self.x = x
		self.y = y
		

class Pose(Position):   

	def __init__(self,x,y,theta):

		Position.__init__(self,x,y)

		self.theta = theta

# workspace consist of Pose
class Workspace():

	def __init__(self,x,y,theta,name):

		self.pose = Pose(x,y,theta)
		self.name = name


class Environment():

	def __init__(self,filename):

		# file_name = rospy.get_param(filename)
		file = open(filename,"r")
		lines =  file.readlines()
		self.database = dict()

		for line in lines:
		
       	            temp = [s.strip() for s in line.split(' ')]
	    	    workspace_name = temp[0]
	    	# convert to float
	    	    x = float(temp[1])
	    	    y = float(temp[2])
	    	    theta = float(temp[3])
			
		    workspace = Workspace(x,y,theta,workspace_name)
		    self.database[workspace_name] = workspace

	def get_workspace(self,name):
		return self.database[name] 

class PathExecutor:
    
    def __init__(self):

	    self.move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	    self.move_base_client.wait_for_server()
	    file_name = rospy.get_param("bnt/goals_file")
	    self.environment = Environment(file_name)
	    rospy.wait_for_service('/move_base/clear_costmaps')
	    self.clear_costmaps = rospy.ServiceProxy('/move_base/clear_costmaps',Empty)

    def run(self):

	    while True:
	        goals = self.get_goals()
	        self.execute_path(goals)

    def get_goals(self):
						
	    loc = raw_input()
	    
	    return [self.environment.get_workspace(s.strip()) for s in loc.split(' ')]
		

    def convert_ws_to_msg(self,workspace):

	    goal = MoveBaseGoal()
	    q = tf.transformations.quaternion_from_euler(0, 0, workspace.pose.theta)
	    goal.target_pose.pose.position.x = workspace.pose.x
	    goal.target_pose.pose.position.y = workspace.pose.y
	    goal.target_pose.pose.orientation.x = q[0]
	    goal.target_pose.pose.orientation.y = q[1]
	    goal.target_pose.pose.orientation.z = q[2]
	    goal.target_pose.pose.orientation.w = q[3]
	    goal.target_pose.header.frame_id = 'map'

	    return goal

    def execute_path(self, path):

	for ws in path:
		msg = self.convert_ws_to_msg(ws)
		self.clear_costmaps()
		self.move_base_client.send_goal(msg)
		finish_before_timeout = self.move_base_client.wait_for_result(rospy.Duration(30))

		if finish_before_timeout:
                     rospy.loginfo("dgdfgdfdgdfgf")
	             state = self.move_base_client.get_state()
	             if state == 3:
	                 rospy.sleep(5)
		else:
		    self.move_base_client.cancel_goal()
		    print "fail to reach the workspace ", ws.name

if __name__ == '__main__':
    rospy.init_node('path_execute')
    path = PathExecutor()
    path.run()
