#!/usr/bin/env python
import numpy as np


# Gets the transformation matrix from end effector to world frame
def getTransform(q):
		# DH parameters
		r1=0.128
		r4=0.1639
		r7=0.0922
		r5=.1157
		d4=0.5716
		d3=0.6127
		re=0.1
		r7=r7+re
		th1=q[0]
		th2=q[1]
		th3=q[2]
		th4=q[3]
		th5=q[4]
		th6=q[5]
		C1 = np.cos(th1)
		S1 = np.sin(th1)
		C2 = np.cos(th2)
		S2 = np.sin(th2)
		T0T211 = C1*C2
		T0T221 = C2*S1
		T0T212 = -C1*S2
		T0T222 = -S1*S2
		C3 = np.cos(th3)
		S3 = np.sin(th3)
		T0T311 = C3*T0T211 + S3*T0T212
		T0T321 = C3*T0T221 + S3*T0T222
		T0T331 = C2*S3 + C3*S2
		T0T312 = C3*T0T212 - S3*T0T211
		T0T322 = C3*T0T222 - S3*T0T221
		T0T332 = C2*C3 - S2*S3
		T0T314 = -T0T211*d3
		T0T324 = -T0T221*d3
		T0T334 = -S2*d3 + r1
		C4 = np.cos(th4)
		S4 = np.sin(th4)
		T0T411 = C4*T0T311 + S4*T0T312
		T0T421 = C4*T0T321 + S4*T0T322
		T0T431 = C4*T0T331 + S4*T0T332
		T0T412 = C4*T0T312 - S4*T0T311
		T0T422 = C4*T0T322 - S4*T0T321
		T0T432 = C4*T0T332 - S4*T0T331
		T0T414 = S1*r4 - T0T311*d4 + T0T314
		T0T424 = -C1*r4 - T0T321*d4 + T0T324
		T0T434 = -T0T331*d4 + T0T334
		C5 = np.cos(th5)
		S5 = np.sin(th5)
		T0T511 = C5*T0T411 + S1*S5
		T0T521 = -C1*S5 + C5*T0T421
		T0T531 = C5*T0T431
		T0T512 = C5*S1 - S5*T0T411
		T0T522 = -C1*C5 - S5*T0T421
		T0T532 = -S5*T0T431
		T0T514 = -T0T412*r5 + T0T414
		T0T524 = -T0T422*r5 + T0T424
		T0T534 = -T0T432*r5 + T0T434
		C6 = np.cos(th6)
		S6 = np.sin(th6)
		T0T611 = C6*T0T511 + S6*T0T412
		T0T621 = C6*T0T521 + S6*T0T422
		T0T631 = C6*T0T531 + S6*T0T432
		T0T612 = C6*T0T412 - S6*T0T511
		T0T622 = C6*T0T422 - S6*T0T521
		T0T632 = C6*T0T432 - S6*T0T531
		T0T711 = T0T611
		T0T721 = T0T621
		T0T731 = T0T631
		T0T712 = T0T612
		T0T722 = T0T622
		T0T732= T0T632
		T0T713= T0T512
		T0T723 = T0T522
		T0T733 = T0T532
		T0T714 = T0T512*r7 + T0T514
		T0T724 = T0T522*r7 + T0T524
		T0T734 = T0T532*r7 + T0T534
		#self.getTransform=np.array([T0T711,T0T721,T0T731,0,T0T712,T0T722,T0T732,0,T0T713,T0T723,T0T733,0,T0T714,T0T724,T0T734,1],dtype=np.float32)
		Transform=np.array([T0T711,T0T712,T0T713,T0T714,T0T721,T0T722,T0T723,T0T724,T0T731,T0T732,T0T733,T0T734,0,0,0,1],dtype=np.float32)
		
		T=np.resize(Transform,(4,4))
		return T


def getJacobian(q):
		# DH parameters
		r1=0.128
		r4=0.1639
		r7=0.0922
		r5=.1157
		d4=0.5716
		d3=0.6127
		re=0.1
		r7=r7+re

		th1=q[0]
		th2=q[1]
		th3=q[2]
		th4=q[3]
		th5=q[4]
		th6=q[5]
		J11 =  d3*np.sin(th1)*np.cos(th2) + d4*np.sin(th1)*np.cos(th2 + th3) + r4*np.cos(th1) - r5*np.sin(th1)*np.sin(th2 + th3 + th4) + r7*np.sin(th1)*np.sin(th5)*np.cos(th2 + th3 + th4) + r7*np.cos(th1)*np.cos(th5)
		J21 =  -d3*np.cos(th1)*np.cos(th2) - d4*np.cos(th1)*np.cos(th2 + th3) + r4*np.sin(th1) + r5*np.sin(th2 + th3 + th4)*np.cos(th1) + r7*np.sin(th1)*np.cos(th5) - r7*np.sin(th5)*np.cos(th1)*np.cos(th2 + th3 + th4)
		J31 =  0
		J41 =  0
		J51 =  0
		J61 =  1
		J12 =  (d3*np.sin(th2) + d4*np.sin(th2 + th3) + r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.cos(th1)
		J22 =  (d3*np.sin(th2) + d4*np.sin(th2 + th3) + r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.sin(th1)
		J32 =  -d3*np.cos(th2) - d4*np.cos(th2 + th3) + r5*np.sin(th2 + th3 + th4) - r7*np.sin(th5)*np.cos(th2 + th3 + th4)
		J42 =  np.sin(th1)
		J52 =  -np.cos(th1)
		J62 =  0
		J13 =  (d4*np.sin(th2 + th3) + r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.cos(th1)
		J23 =  (d4*np.sin(th2 + th3) + r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.sin(th1)
		J33 =  -d4*np.cos(th2 + th3) + r5*np.sin(th2 + th3 + th4) - r7*np.sin(th5)*np.cos(th2 + th3 + th4)
		J43 =  np.sin(th1)
		J53 =  -np.cos(th1)
		J63 =  0
		J14 =  (r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.cos(th1)
		J24 =  (r5*np.cos(th2 + th3 + th4) + r7*np.sin(th5)*np.sin(th2 + th3 + th4))*np.sin(th1)
		J34 =  r5*np.sin(th2 + th3 + th4) - r7*np.sin(th5)*np.cos(th2 + th3 + th4)
		J44 =  np.sin(th1)
		J54 =  -np.cos(th1)
		J64 =  0
		J15 =  -r7*(np.sin(th1)*np.sin(th5) + np.cos(th1)*np.cos(th5)*np.cos(th2 + th3 + th4))
		J25 =  r7*(-np.sin(th1)*np.cos(th5)*np.cos(th2 + th3 + th4) + np.sin(th5)*np.cos(th1))
		J35 =  -r7*np.sin(th2 + th3 + th4)*np.cos(th5)
		J45 =  np.sin(th2 + th3 + th4)*np.cos(th1)
		J55 =  np.sin(th1)*np.sin(th2 + th3 + th4)
		J65 =  -np.cos(th2 + th3 + th4)
		J16 =  0
		J26 =  0
		J36 =  0
		J46 =  np.sin(th1)*np.cos(th5) - np.sin(th5)*np.cos(th1)*np.cos(th2 + th3 + th4)
		J56 =  -np.sin(th1)*np.sin(th5)*np.cos(th2 + th3 + th4) - np.cos(th1)*np.cos(th5)
		J66 =  -np.sin(th5)*np.sin(th2 + th3 + th4)
		#self.getJacobian=np.array([J11,J21,J31,J41,J51,J61, J12,J22,J32,J42,J52,J62,J13, J23,J33,J43,J53,J63, J14,J24,J34,J44,J54,J64, J15,J25,J35,J45,J55,J65, J16,J26,J36,J46,J56,J66] ,dtype=np.float32)
		Jacobian=np.array([J11,J12,J13,J14,J15,J16, J21,J22,J23,J24,J25,J26,J31, J32,J33,J34,J35,J36, J41,J42,J43,J44,J45,J46, J51,J52,J53,J54,J55,J56, J61,J62,J63,J64,J65,J66] ,dtype=np.float32)

		J=np.resize(Jacobian,(6,6))
		return J

'''
				FUNCTION: FIFO Buffer
//******************************************************************************************************************************************************
Inputs: 1.  The current buffer ForceBuffer
		      2. The measurement to be addaed to the buffer
		
Outputs:  ForceBuffer

Summary this function places the measurement into the buffer while eliminated the oldsest measurement

Function by (c) 2013 Philip Long
//*******************************************************************************************************************************************************

'''


def fifoBufferInsert(ResolvedForce,ForceBuffer):
	S=ForceBuffer.shape
	ForceBufferFunction=ForceBuffer
	
	for i in reversed(range(S[0])): # This should be going backards
		
		for j in range(S[1]):
			
			if i>0:
			    ForceBufferFunction[i][j]=ForceBufferFunction[i-1][j] # Replace ith row with ith-1 row	
			else:
			    ForceBufferFunction[i][j]=ResolvedForce[j] # First row is new measurement   
	return ForceBufferFunction

'''
				FUNCTION: LowPassFilter
//******************************************************************************************************************************************************
Inputs: 1.  ForceBuffer

Outputs:  MovingAverageForce

This function simply gets the average of the readings in the buffer to filter out the noise

Function by (c) 2013 Philip Long
//*******************************************************************************************************************************************************

'''


def LowPassFilter(ForceBuffer):

	S=ForceBuffer.shape
	MovingAverageForce=np.zeros(6)
	for i in range(S[1]):
	    sum=0
 
	    for j in range(S[0]):
		sum=sum+ForceBuffer[j][i]

	    MovingAverageForce[i]=sum/(S[0])
    
	return MovingAverageForce


