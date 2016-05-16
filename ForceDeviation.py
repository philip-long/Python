#!/usr/bin/env python

import time
import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import WrenchStamped
from ur_msgs.msg import IOStates
import timeit
from ur_driver.io_interface import *
from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import numpy as np
import IRT_Functions as my
# This node publishes the signal to inflate or deflate the unviersal gripper

# initialise both flags as flase since there is no way to know

'''
		Program to implement a Cartesian stiffness strategy
		
		K changes the stiffness in each Cartesian direction

		Limit is the lower limit of actuation i.e if Limit[1]=50, forces under 50 newtons in the y direction will be ignored
		this is necessary due to the poor quality of our force readings. This can be overcome by adding a secondary force sensor
		or better taking into account the dynamic of the arm

		ForceBuffer is the low pass filter. The higher the number of rows the smoother the force but the less reactive the system becomes
		again this is due to the poor quality of the sensor and the high frequency noise present

		The force is transformed into a joint torque using the Jacobian. 

'''


class forcedeviationlistener:
    def __init__(self):
        self.getforce=-1 # initialise the states
        self.getq=-1
        self.getN=-1
        self.getjoints=-1
        # subscribe to frontleft prox
        rospy.Subscriber('wrench', WrenchStamped, self.valuesForce) # Subscribe to the robot IO states
        rospy.Subscriber('joint_states', JointState, self.valuesJoint) # Subscribe to the robot IO states

    def valuesForce(self, msg):        # Define the function to get the values       
        self.getforce = [msg.wrench.force.x, msg.wrench.force.y,msg.wrench.force.z,msg.wrench.torque.x, msg.wrench.torque.y,msg.wrench.torque.z ]
    def valuesJoint(self, msg):        # Define the function to get the values
	self.getq=msg.position
	self.getN=msg.name
	self.getjoints=msg
	
# Beginning of main program	  

def main():  



    JointDeviation=np.zeros(6)
    Rate=1./400.
    K=np.array([0.005,0.005,0.005,0.0005,0.0005,0.0005]) # Stiffness
    Limit=np.array([30.,30.,30.,15.,15.,15.])
    ForceBuffer=np.zeros((300,6))
    Favg=np.array([0.0,0.0,0.0,0.0,0.0,0.])
    
    try:

	rospy.init_node('ForceDev')
	listener = forcedeviationlistener() # Get data from other nodes
	pubDeviation = rospy.Publisher('Deviation', Floats,queue_size=10)  

    
	while not rospy.is_shutdown(): 
	    
	    F=np.array([0.0,0.0,0.0,0.0,0.0,0.])
	    
	    
	    F=np.array(listener.getforce) # Put data in a reasonable format

	    if listener.getq!=-1:

	      T=my.getTransform(listener.getq)
	      J=my.getJacobian(listener.getq)
	      
	      
			
              ForceBuffer=my.fifoBufferInsert(F,ForceBuffer)
              Favg=my.LowPassFilter(ForceBuffer)
	      
	      for i in range(6): # Reduce the amount of force
		    Favg[i]=K[i]*Favg[i]
	    
	      JointDeviation=np.dot(J.transpose(),Favg) # compute Force deviation    
		    
	    pubDeviation.publish(JointDeviation)
	    
	    rospy.sleep(Rate)
	    
    except KeyboardInterrupt:
        print "interupted"
	rospy.signal_shutdown("KeyboardInterrupt")
	raise
 
if __name__ == '__main__': main()
