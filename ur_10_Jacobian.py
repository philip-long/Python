#!/usr/bin/env python


'''

author: Philip Long
'''

import sys, os
import sympy
from pylab import array, norm
import re
import multiprocessing as mp
import argparse




Axis=["x","y","z"]

def skew(u): # returns the skew operator
    return sympy.Matrix([[0,-u[2],u[1]],[u[2],0,-u[0]],[-u[1],u[0],0]])

def simp_matrix(M): #olivier's function thanks!!
    '''
    simplify matrix for old versions of sympy
    '''
    for i in xrange(M.rows):
        for j in xrange(M.cols):
            M[i,j] = sympy.simplify(M[i,j])
    return M

def TransMat(y,Type,out): # returns the homogenous transformation matrix
    if Type in ['Rx','RX','x','rx','Ry','Ry','y','ry','Rz','Rz','z','rz']:
        if Type in ['Rx','RX','x','rx']:
                T=sympy.Matrix([[1.0, 0.0,0.0,0.0],[0.0,sympy.cos(y),-sympy.sin(y),0.0], [0.0,sympy.sin(y),sympy.cos(y),0.0],[0.0,0.0,0.0,1.0]])
        elif Type in ['Ry','Ry','y','ry']:
                T=sympy.Matrix([[sympy.cos(y),  0.0,      sympy.sin(y), 0.0], [0.0,       1.0,      0.0,      0.0], [-sympy.sin(y), 0.0,      sympy.cos(y), 0.0], [0.0,       0.0    ,  0.0,      1.0] ])
        elif  Type in ['Rz','Rz','z','rz']:
                T=sympy.Matrix([[sympy.cos(y),-sympy.sin(y), 0.0, 0.0], [sympy.sin(y),sympy.cos(y), 0.0,0.0], [0.0, 0.0,1.0,0.0], [0.0, 0.0, 0.0,      1.0] ])
        else:
                print 'Invalid rotation input must be Rx, Ry Rz'


    elif Type in ['t','trans','p']:
        T=sympy.Matrix([[1.0,0.0,0.0, y[0]], [0.0,1.0, 0.0,y[1]], [0.0, 0.0,1.0,y[2]], [0.0,0.0,0.0,1.0] ])
    else:

        print ' Improper input,'
        print 'y has one entry for rotation and 3 entries for translation'

    if out in ['R','Rot','r','rot']:
        return T[0:3,0:3]
    else:
        return T

def RPY_to_Rot(u,out): # Converts RPY to Rotational cosine
    phi1=u[0]
    theta1=u[1]
    psi1=u[2]
    if out in ['R','Rot','r','rot']:
        return TransMat(phi1,'x','rot')*TransMat(theta1,'y','rot')*TransMat(psi1,'z','rot')
    else:
        return TransMat(phi1,'x','T')*TransMat(theta1,'y','T')*TransMat(psi1,'z','T')

def DGM_ij(R,t,q):  # returns the transformation matrix from each frame to antecedent
    T=[]

    for i in range(6):
        T.append(t[i]*R[i]*TransMat(q[i],rq[i],'T'))

    return T

def DGM(R,t,q): # returns the transformation matrix from each frame to world
    T=[]
    Tpre=sympy.eye(4)
    for i in range(6):
        T.append(t[i]*R[i]*TransMat(q[i],rq[i],'T'))
        T[i]=Tpre*T[i]
        T[i]=simp_matrix(T[i])
        Tpre=T[i]
    return T

def DKM(T,rq,frame): # returns the transformation matrix from each frame to world

    J0n=sympy.zeros(6,frame)

    for k in range(frame):

        a=T[k][0:3,Axis.index(rq[k])]

        askew=skew(a)

        J=askew*( T[frame-1][0:3,3]-T[k][0:3,3])

        J=J.col_join(a)

        J0n[:,k]=J

    return J0n


if __name__ == '__main__':
    # Robot Definition
    R=[]
    t=[]
    rq=[]
    R.append(RPY_to_Rot([0.0,0.0,0.0],"T")) # Rotation matrix from j to j-1
    t.append(TransMat([0.0,0.0,0.1273],"t","T")) # Translation from j to j-1
    rq.append("z") # axis of joint

    # upper_arm_link to shoulder_link
    R.append(RPY_to_Rot([0.0, sympy.pi/2, 0.0],"T"))
    t.append(TransMat([0.0, 0.220941, 0.0],"t","T"))
    rq.append("y")

    # forearm_link to upper_arm_link
    R.append(RPY_to_Rot([0.0, 0.0, 0.0],"T"))
    t.append(TransMat([0.0, -0.1719, 0.612],"t","T"))
    rq.append("y")

    # wrist_1_link to forearm_link
    R.append(RPY_to_Rot([0.0, sympy.pi/2, 0.0],"T"))
    t.append(TransMat([0.0, 0.0, 0.5723],"t","T"))
    rq.append("y")

    # wrist_2_link to wrist_1_link
    R.append(RPY_to_Rot([0.0, 0.0, 0.0],"T"))
    t.append(TransMat([0.0, 0.1149, 0.0],"t","T"))
    rq.append("z")

    # wrist_3_link to wrist_2_link
    R.append(RPY_to_Rot([0.0, 0.0, 0.0],"T"))
    t.append(TransMat([0.0, 0.0, 0.1157],"t","T"))
    rq.append("y")


    q=[]

    q1,q2,q3,q4,q5,q6=sympy.symbols("q1 q2 q3 q4 q5 q6")
    q.append(q1)
    q.append(q2)
    q.append(q3)
    q.append(q4)
    q.append(q5)
    q.append(q6)

    frame=6
    T=DGM(R, t, q)
    for k in range(6):
        frame=k+1;
        J=DKM(T,rq,frame)
        J=simp_matrix(J)
        for i in range(6):
            for j in range (frame):
                    print "J0"+str(frame)+"[",i,"][",j,"]=",J[i,j],"; "
            print "\n"

    for i in range(6):
        for j in range (4):
            for k in range (4):
                print "T0"+str(i+1)+"[",j,"][",k,"]=",T[i][j,k],"; "
        print "\n"



    print J
