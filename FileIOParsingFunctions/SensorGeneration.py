# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:51:09 2015

@author: philip
"""

# We need the radius and length of each link
# Each cylinder is normal

# Base_link



import lxml.etree as ltr
import numpy as np
from tf import transformations

def create_sensor(root,number_of_sensor,angle,min_range,max_range,Rate):
    name_of_sensor="ir_sharp_"+str(number_of_sensor)
    topicname="/ir/"+name_of_sensor
    plugin_name=name_of_sensor+"_controller"
    name_of_link="ir_sharp_"+str(number_of_sensor)+"_link"
    
    GAZEBO=ltr.SubElement(root,"gazebo",reference=name_of_link)
    GAZEBO.insert(0,ltr.Comment(name_of_sensor))  
    SENSOR=ltr.SubElement(GAZEBO,"sensor",type="ray",name=name_of_sensor)
    POSE = ltr.SubElement(SENSOR, "pose")
    POSE.text = str(0) +" "+str(0)+" "+str(0)+" "+ str(0)+" "+str(0)+" "+str(0)
    VISUALIZE=ltr.SubElement(SENSOR,"visualize")
    VISUALIZE.text="true"
    UPDATE_RATE=ltr.SubElement(SENSOR,"update_rate")
    UPDATE_RATE.text=str(Rate)
    RAY=ltr.SubElement(SENSOR,"ray")
    SCAN=ltr.SubElement(RAY,"scan")
    HORIZONTAL=ltr.SubElement(SCAN,"horizontal")
    SAMPLES=ltr.SubElement(HORIZONTAL,"samples")
    SAMPLES.text="10"
    RESOLUTION=ltr.SubElement(HORIZONTAL,"resolution")
    RESOLUTION.text="1"
    MIN_ANGLE=ltr.SubElement(HORIZONTAL,"min_angle")
    MIN_ANGLE.text=str(0)
    MAX_ANGLE=ltr.SubElement(HORIZONTAL,"max_angle")
    MAX_ANGLE.text=str(angle)
    RANGE=ltr.SubElement(RAY,"range")
    MIN_RANGE=ltr.SubElement(RANGE,"min")
    MIN_RANGE.text=str(min_range)
    MAX_RANGE=ltr.SubElement(RANGE,"max")
    MAX_RANGE.text=str(max_range)
    RESOLUTION_RANGE=ltr.SubElement(RANGE,"resolution")
    RESOLUTION_RANGE.text=str(0.01)
    PLUGIN=ltr.SubElement(SENSOR,"plugin",name=plugin_name,filename="libgazebo_ros_laser.so")
    TOPICNAME=ltr.SubElement(PLUGIN,"topicName")
    TOPICNAME.text=topicname
    FRAME_NAME=ltr.SubElement(PLUGIN,"frameName")
    FRAME_NAME.text=name_of_link
    return root

def create_box(root,x,y,z):
    GEOMETRY = ltr.SubElement(root,"geometry")
    BOX = ltr.SubElement(GEOMETRY,"box",size=str(x) +" "+str(y)+" "+str(z))
    return root
    
    
   
def create_sensor_link(frame_name,number_of_sensor,Pose):
    x,y,z,Rx,Ry,Rz=Pose
    name_of_link="ir_sharp_"+str(number_of_sensor)+"_link"
    name_of_joint="ir_sharp_"+str(number_of_sensor)+"_joint"
    
    # Create joint first
    JOINT= ltr.Element("joint",name=name_of_joint,type="fixed") 
    AXIS=ltr.SubElement(JOINT,"axis")
    XYZ = ltr.SubElement(AXIS,"xyz")
    XYZ.text = str(0) +" "+str(1)+" "+str(0)+" "
    ORIGIN= ltr.SubElement(JOINT,"origin",xyz=str(x) +" "+str(y)+" "+str(z)+" ",rpy= str(Rx) +" "+str(Ry)+" "+str(Rz)+" ")   
    PARENT = ltr.SubElement(JOINT,"parent",link="${prefix}"+frame_name)
    CHILD = ltr.SubElement(JOINT,"child",link=name_of_link)


    # Now create link
    LINK= ltr.Element("link",name=name_of_link,type="fixed") 
    
    # Link: Collision 
    COLLISION=ltr.SubElement(LINK,"collision")
    #ORIGIN= ltr.SubElement(COLLISION,"origin")   
    #XYZ = ltr.SubElement(ORIGIN,"xyz")
    #XYZ.text = str(x) +" "+str(y)+" "+str(z)+" "
    #RXRYRZ = ltr.SubElement(ORIGIN,"rpy")
    #RXRYRZ.text = str(Rx) +" "+str(Ry)+" "+str(Rz)+" "    
    create_box(COLLISION,0.008,0.04,0.01)
    # Link: Visual 
    VISUAL=ltr.SubElement(LINK,"visual")
    #ORIGIN= ltr.SubElement(VISUAL,"origin")   
    #XYZ = ltr.SubElement(ORIGIN,"xyz")
    #XYZ.text = str(x) +" "+str(y)+" "+str(z)+" "
    #RXRYRZ = ltr.SubElement(ORIGIN,"rpy")
    #RXRYRZ.text = str(Rx) +" "+str(Ry)+" "+str(Rz)+" "
    create_box(VISUAL,0.008,0.04,0.01)
    
    # Link: inertial
    
    INERTIAL= ltr.SubElement(LINK, "inertial")
    MASS = ltr.SubElement(INERTIAL,"mass",value=str("1e-5"))     
    INERTIA = ltr.SubElement(INERTIAL,"inertia", ixx = str("1e-6"),ixy =str("0"),ixz = str("0"), iyy= str("1e-6"),iyz = str("0"), izz= str("1e-6"))
    ACM=ltr.Element("disable_collisions",link1=frame_name,link2=name_of_link, reason="Adjacent") 
    
    return JOINT,LINK,ACM
    
def create_obstacle_link(frame_name,number_of_sensor,Pose):
    x,y,z,Rx,Ry,Rz=Pose
    name_of_link="ir_sharp_"+str(number_of_sensor)+"_link"
    name_of_joint="ir_sharp_"+str(number_of_sensor)+"_joint"
    
    # Create joint first
    JOINT= ltr.Element("joint",name=name_of_joint,type="fixed") 
    AXIS=ltr.SubElement(JOINT,"axis")
    XYZ = ltr.SubElement(AXIS,"xyz")
    XYZ.text = str(0) +" "+str(1)+" "+str(0)+" "
    ORIGIN= ltr.SubElement(JOINT,"origin",xyz=str(x) +" "+str(y)+" "+str(z)+" ",rpy= str(Rx) +" "+str(Ry)+" "+str(Rz)+" ")   
    PARENT = ltr.SubElement(JOINT,"parent",link="${prefix}"+frame_name)
    CHILD = ltr.SubElement(JOINT,"child",link=name_of_link)


    # Now create link
    LINK= ltr.Element("link",name=name_of_link,type="fixed") 
    
    # Link: Collision 
    COLLISION=ltr.SubElement(LINK,"collision")
    #ORIGIN= ltr.SubElement(COLLISION,"origin")   
    #XYZ = ltr.SubElement(ORIGIN,"xyz")
    #XYZ.text = str(x) +" "+str(y)+" "+str(z)+" "
    #RXRYRZ = ltr.SubElement(ORIGIN,"rpy")
    #RXRYRZ.text = str(Rx) +" "+str(Ry)+" "+str(Rz)+" "    
    create_box(COLLISION,0.05,0.05,0.03)
    # Link: Visual 
    VISUAL=ltr.SubElement(LINK,"visual")
    #ORIGIN= ltr.SubElement(VISUAL,"origin")   
    #XYZ = ltr.SubElement(ORIGIN,"xyz")
    #XYZ.text = str(x) +" "+str(y)+" "+str(z)+" "
    #RXRYRZ = ltr.SubElement(ORIGIN,"rpy")
    #RXRYRZ.text = str(Rx) +" "+str(Ry)+" "+str(Rz)+" "
    create_box(VISUAL,0.05,0.05,0.03)
    
    # Link: inertial
    
    INERTIAL= ltr.SubElement(LINK, "inertial")
    MASS = ltr.SubElement(INERTIAL,"mass",value=str("1e-5"))     
    INERTIA = ltr.SubElement(INERTIAL,"inertia", ixx = str("1e-6"),ixy =str("0"),ixz = str("0"), iyy= str("1e-6"),iyz = str("0"), izz= str("1e-6"))
    ACM=ltr.Element("disable_collisions",link1=frame_name,link2=name_of_link, reason="Adjacent") 
        

def create_sensors_for_face(XACRO,SensorCount,face_array,string_joint_link,string_collisions):
    
    Number_of_sensors=len(face_array.Sensors)
    frame_name=face_array.frame_name
    Position_min=face_array.Position_min
    Position_max=face_array.Position_max
    
    Pose=Position_min
    
    for j in range(Number_of_sensors):
        
        angle=face_array.Sensors[j].angle
        min_range=face_array.Sensors[j].min_range
        max_range=face_array.Sensors[j].max_range
        Rate=face_array.Sensors[j].Rate
        
        Pose=Pose+ ((Position_max-Position_min)/Number_of_sensors)
        JOINT,LINK,ACM=create_sensor_link(frame_name,SensorCount,Pose) # create joint,link and ACM entry
        create_sensor(XACRO,SensorCount,angle,min_range,max_range,Rate) # create sensor            
        
        jointstring=ltr.tostring(JOINT, pretty_print=True) # convert xml tree to string
        linkstring=ltr.tostring(LINK, pretty_print=True) # convert xml tree to string
        acmstring=ltr.tostring(ACM, pretty_print=True) # convert xml tree to string         
        string_joint_link=string_joint_link+jointstring+linkstring+"\n" # append string to previous string
        string_collisions=string_collisions+acmstring+""    
        SensorCount+=1
    
    return string_joint_link,string_collisions,XACRO,SensorCount

# Now Write my xacro file


class Sensor_attributes:
    def __init__(self,width,min_range,max_range,Rate):
        self.min_range = min_range
        self.max_range = max_range
        self.Rate = Rate
        self.angle=(np.arctan(width/max_range));  

class sensor_array:
    def __init__(self,frame_name,Position_min,Position_max,Sensors):
        self.frame_name = frame_name
        self.Position_min = Position_min
        self.Position_max = Position_max
        self.Sensors=Sensors        
        
        
    

def main(): 
          
    # Header of the sensor file
    NSMAP = {"xacro" : "http://www.ros.org/wiki/xacro"}                      
    ROOT = ltr.Element("robot",nsmap=NSMAP) 
    XACRO= ltr.SubElement(ROOT,"xacroCOLONmacro",name="ur10_arm_gazebo",params="prefix")
    ROOT.insert(0,ltr.Comment("Proximity sensors"))
    string_joint_link=""
    string_collisions=""
    modify=True #if false the original files are used by moveit if true the file with sensor is used
    
    SensorCount=0    
    width=0.10; min_range=0.06;    max_range=0.8;       Rate=10; theta_incline=0.05           
    s=Sensor_attributes(width,min_range,max_range,Rate)
    
    
#     
    
    
    
    # Link 2  
    frame_name="forearm_link" 
      
#    Note 1 In the absence of an array pick max position     
#    Note 2 R is defined by relative rotations
    # Ultrasound ring 
    # 0  
    theta_incline=15.* np.pi/180.
    R=np.dot(np.dot(transformations.rotation_matrix(np.pi/2,np.array([1,0,0])),transformations.rotation_matrix(np.pi/2,np.array([0,0,1]))),transformations.rotation_matrix(-np.pi,np.array([0,1,0])))
    Rincline=np.dot(R,transformations.rotation_matrix(-theta_incline,np.array([0,0,1]))) 
    Rx,Ry,Rz=transformations.euler_from_matrix(Rincline,'sxyz')
    Position_min=np.array([-0.06,-0.06,0.53,Rx,Ry,Rz]);    Position_max=np.array([0.078,0.00,0.48,Rx,Ry,Rz])   
    face_array=sensor_array(frame_name,Position_min,Position_max,[s])     
    string_joint_link,string_collisions,XACRO,SensorCount=create_sensors_for_face(XACRO,SensorCount,face_array,string_joint_link,string_collisions)
    print "Generated Sensor ",SensorCount 
    
#    # 1 to mod
    R=np.dot(np.dot(transformations.rotation_matrix(np.pi/2,np.array([1,0,0])),transformations.rotation_matrix(np.pi/2,np.array([0,0,1]))),transformations.rotation_matrix(-np.pi,np.array([0,1,0])))
    R=np.dot(R,transformations.rotation_matrix(-np.pi/2,np.array([1,0,0]))) # rotating for the ring
    Rincline=np.dot(R,transformations.rotation_matrix(-theta_incline,np.array([0,0,1]))) 
    Rx,Ry,Rz=transformations.euler_from_matrix(Rincline,'sxyz')
    
    Position_min=np.array([-0.06,-0.06,0.53,Rx,Ry,Rz]);    Position_max=np.array([0.0,0.075,0.48,Rx,Ry,Rz])   

    face_array=sensor_array(frame_name,Position_min,Position_max,[s])     
    string_joint_link,string_collisions,XACRO,SensorCount=create_sensors_for_face(XACRO,SensorCount,face_array,string_joint_link,string_collisions)
    print "Generated Sensor ",SensorCount 
#    
#    #2
#    
    R=np.dot(np.dot(transformations.rotation_matrix(np.pi/2,np.array([1,0,0])),transformations.rotation_matrix(np.pi/2,np.array([0,0,1]))),transformations.rotation_matrix(-np.pi,np.array([0,1,0])))
    R=np.dot(R,transformations.rotation_matrix(-np.pi,np.array([1,0,0]))) # rotating for the ring
    Rincline=np.dot(R,transformations.rotation_matrix(-theta_incline,np.array([0,0,1]))) 
    Rx,Ry,Rz=transformations.euler_from_matrix(Rincline,'sxyz')
    
    Position_min=np.array([-0.06,-0.06,0.53,Rx,Ry,Rz]);    Position_max=np.array([-0.075,-0.0,0.48,Rx,Ry,Rz])   

    face_array=sensor_array(frame_name,Position_min,Position_max,[s])     
    string_joint_link,string_collisions,XACRO,SensorCount=create_sensors_for_face(XACRO,SensorCount,face_array,string_joint_link,string_collisions)
    print "Generated Sensor ",SensorCount 
#    
#    #3
    R=np.dot(np.dot(transformations.rotation_matrix(np.pi/2,np.array([1,0,0])),transformations.rotation_matrix(np.pi/2,np.array([0,0,1]))),transformations.rotation_matrix(-np.pi,np.array([0,1,0])))
    R=np.dot(R,transformations.rotation_matrix(np.pi/2,np.array([1,0,0]))) # rotating for the ring
    Rincline=np.dot(R,transformations.rotation_matrix(-theta_incline,np.array([0,0,1]))) 
    Rx,Ry,Rz=transformations.euler_from_matrix(Rincline,'sxyz')
    
    Position_min=np.array([-0.06,-0.06,0.53,Rx,Ry,Rz]);    Position_max=np.array([0.0,-0.075,0.48,Rx,Ry,Rz])   

    face_array=sensor_array(frame_name,Position_min,Position_max,[s])     
    string_joint_link,string_collisions,XACRO,SensorCount=create_sensors_for_face(XACRO,SensorCount,face_array,string_joint_link,string_collisions)
    print "Generated Sensor ",SensorCount 
#    
    # -------------------------------------------------------------------------
    #
    #       Convert to text, Replace Colons and write result to .xacro file 
    #
    # -------------------------------------------------------------------------

    Original_xacro_file = open("/home/philip/catkin_ws_v5/src/ur_package/config/SensorGeneration/ur10.urdf.xacro", "r") # Bare version of .xacro
    Original_srdf_file = open("/home/philip/catkin_ws_v5/src/ur_package/config/SensorGeneration/ur10.srdf", "r") # Bare version of .sdf

    Gazebo_sensor_file = open("/opt/ros/indigo/share/ur_description/urdf/ur10.gazebo.xacro", 'w')    
    UR10_xacro_file = open("/opt/ros/indigo/share/ur_description/urdf/ur10.urdf.xacro", "w") # replace used version with sensor version
    UR10_srdf_file = open("/opt/ros/indigo/share/ur10_moveit_config/config/ur10.srdf", "w")
    
    
    contents = Original_srdf_file.readlines() # read bare version 
    if(modify):
        contents.insert(-1,string_collisions) # insert the supplmentary joint information at end of file
    contents = "".join(contents) # joint contents to create buffer
    UR10_srdf_file.write(contents) # write buffer to used version 
    
    
    contents = Original_xacro_file.readlines() # read bare version 
    if(modify):
        contents.insert(-6,string_joint_link) # insert the supplmentary joint information at end of file
    contents = "".join(contents) # joint contents to create buffer
    UR10_xacro_file.write(contents) # write buffer to used version 
    
    
    string=ltr.tostring(ROOT, pretty_print=True,xml_declaration=True)
    Gazebo_sensor_file.write(string.replace("COLON",":")) # A terrible hack I should be ashamed of required cause I couldn't be bothered learning more about namespaces
    
    
    
    Gazebo_sensor_file.close()
    Original_srdf_file.close()
    Original_xacro_file.close()
    UR10_xacro_file.close()
    UR10_srdf_file.close()


if __name__ == '__main__': main()