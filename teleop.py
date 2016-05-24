#!/usr/bin/env python

# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Willow Garage, Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import rospy

import numpy as np
from geometry_msgs.msg import TwistStamped
import tf
import Transformations as my

import sys, select, termios, tty

msg = """
Control Your Turtlebot!
---------------------------
Moving around:
   x    y    z    Position
   a    b    c    Orientation
   m              Switch Direction
   o              Zero Velocity
V/v : increase/decrease max speeds by 10%
T/t : increase/decrease only linear speed by 10%
R/r : increase/decrease only angular speed by 10%
f   : change the frame of motion from tool to world
space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""

moveBindings = {
        'x': (1, 0, 0, 0, 0, 0),
        'y': (0, 1, 0, 0, 0, 0),
        'z': (0, 0, 1, 0, 0, 0),
        'a': (0, 0, 0, 1, 0, 0),
        'b': (0, 0, 0, 0, 1, 0),
        'c': (0, 0, 0, 0, 0, 1),
        'o': (0, 0, 0, 0, 0, 0),
           }

speedBindings={
        'V':(1.1,1.1),
        'v':(.9,.9),
        'T':(1.1,1),
        't':(.9,1),
        'R':(1,1.1),
        'r':(1,.9),
          }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = .1
turn = 0.5

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":

    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop')
    pub = rospy.Publisher('velocity', TwistStamped, queue_size=5)
    rot=[]
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    dX=[0,0,0,0,0,0]
    direction=1
    changeframe=1
    R=np.identity(4)
    Screw=np.zeros(6)
    A=np.zeros(shape=(3,6))
    B=np.zeros(shape=(3,6))
    dXnp=np.array([0.0, 0.0 ,0.0, 0.0, 0.0, 0.0])
    listener = tf.TransformListener()
    try:

        print vels(speed,turn)

        while (1):


            try:
                listener.waitForTransform("/base_link", "/ee_link", rospy.Time(), rospy.Duration(4.0))
                (trans,rot) = listener.lookupTransform('/base_link', '/ee_link', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                print "not available"



            key = getKey()

            if key in moveBindings.keys():
                dX = moveBindings[key]
                count = 0

            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0
                print vels(speed,turn)
                if (status == 14):
                    print msg
                status = (status + 1) % 15

            elif key=='m':
                direction=-1*direction
                count = 0
            elif key=='f':
                changeframe=-1*changeframe
                count = 0
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break

            target_speed = speed
            target_turn = turn

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            twist = TwistStamped();

            for i in range(6):
                dXnp[i] = dX[i]


            if(changeframe!=1): # Change the frame of the veloccity
                R=my.quaternion_matrix([rot[3],rot[0],rot[1],rot[2]])
                A=np.concatenate((R[0:3][:,0:3],np.zeros(shape=(3,3))),1)
                B=np.concatenate((np.zeros(shape=(3,3)),R[0:3][:,0:3]),1)
                Screw=np.vstack((A,B))
                dXnp=np.dot(Screw,dXnp)

            twist.twist.linear.x = control_speed*dXnp[0]* direction;
            twist.twist.linear.y = control_speed*dXnp[1]* direction;
            twist.twist.linear.z = control_speed*dXnp[2]* direction;
            twist.twist.angular.x = control_turn*dXnp[3]* direction;
            twist.twist.angular.y = control_turn*dXnp[4]* direction;
            twist.twist.angular.z = control_turn*dXnp[5]* direction;
            
            pub.publish(twist)

            #print("loop: {0}".format(count))
            #print("target: vx: {0}, wz: {1}".format(target_speed, target_turn))
            #print("publihsed: vx: {0}, wz: {1}".format(twist.linear.x, twist.angular.z))

    except:
        print "error"

    finally:
        twist = TwistStamped();
        twist.twist.linear.x = 0; twist.twist.linear.y = 0; twist.twist.linear.z = 0
        twist.twist.angular.x = 0; twist.twist.angular.y = 0; twist.twist.angular.z = 0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
