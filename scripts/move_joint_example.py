#!/usr/bin/python

'''
This is an example node for moving the joints.
'''

import sys, rospy

from rospy.exceptions import ROSInterruptException
from rospy import ServiceException
from myp_ros.msg import *
from myp_ros.srv import *

'''
Initialize the node.
'''
rospy.init_node('move_joint_example')

'''
Wait for the connection service to be provided by the PRob.
Connect to the PRob using this service.
Print out the response.
'''
rospy.wait_for_service('connect')
connect = rospy.ServiceProxy('connect', ConnectionCommand)
resp = connect('real', 'PRob2R', 'normal')
rospy.loginfo(resp.message)

'''
Initialize the move_joint service proxy.
'''
move_joint = rospy.ServiceProxy('move_joint', MoveJoint)

'''
Define a function to return to neutral position to be called on shutdown.
In shutdwon ROS services cannot provide the return value so we may use
the ServiceException raised by this as the trigger for service completion.
'''
def move_back():
	rospy.loginfo("Moving back...")
	try:
		move_joint(actuator_ids=['1', '2', '3', '4', '5', '6'], 
				   position=[0]*6, velocity = [80]*6, acceleration = [80]*6)
	except ServiceException as exception:
		rospy.loginfo("Done. Goodbye!")


actuator_ids = ['1', '2', '3', '4', '5', '6']
vals = [0 + i*2 for i in range(10)]
velocity = [80]*6
acceleration = [80]*6

i = 0
r = rospy.Rate(10) # 10hz

while not rospy.is_shutdown():
	val = vals[i % len(vals)]

	position = [val, val, val, val, val, val]
	try:
		resp = move_joint(actuator_ids=actuator_ids,
						  position=position, velocity=velocity, acceleration=acceleration)

	except ROSInterruptException as error:
		rospy.loginfo("Movement interrupted by shutdown.")
		move_back()

	rospy.loginfo(resp.message)
	i += 1
	r.sleep()


