# This program is created to convert Nabils nodes to something usable in Adams
# First Pass is to put point masses at the desired location of Nodes
# After we place springs in between them
# Using csv import for elements as must do a little bit more manipulation

# Preamble
# In order to facilatate the program nodes.txt and elements.txt must be saved as a .csv  file with ',' as delimiter

import os
import csv
import tkFileDialog
import time

# Input is a comma seperated csv file 


# ---------------------------------------------------------------------------------
# For loop one Inserting nodes
# ---------------------------------------------------------------------------------
Output='DataNew.txt'

Out=open(Output,'w')
Force=5
Damping=100.0 #Desired Damping between springs
Counter=1 # Total number of point masses created
AdamsID=100

with open('NodesNew.csv', 'rb') as N:
    
       
    ReadNodes = csv.reader(N, delimiter=',', quoting=csv.QUOTE_NONE)
        
    for line in ReadNodes: 
        
    
    # Writing to create a point mass at this location, this data corresponds to Adams format
    # We use Counter to define point mass name, adams id
    # Max Adams id of model in which we import the deformable object is 100, therefore we start at 101

        Mass=line[3]
       
        Out.write('! \n\
!-------------------------------- POINT_MASS_'+str(Counter)+'--------------------------------! \n\
! \n\
! \n\
defaults coordinate_system  & \n\
default_coordinate_system = .CooperativeControls.ground \n\
! \n\
part create point_mass name_and_position  & \n\
point_mass_name = .CooperativeControls.POINT_MASS_'+str(Counter)+'  & \n\
adams_id = '+str(AdamsID)+'   & \n\
location ='+str(line[0])+','+str(line[1])+','+str(line[2])+' & \n\
orientation = 0.0d, 0.0d, 0.0d \n\
! \n\
! \n\
defaults coordinate_system  & \n\
default_coordinate_system = .CooperativeControls.POINT_MASS_'+str(Counter)+'\n\
! \n\
! ****** Markers for current part ****** \n\
! \n\
marker create  &\n\
   marker_name = .CooperativeControls.POINT_MASS_'+str(Counter)+'.cm  &\n\
   adams_id = '+str(AdamsID)+'  &\n\
   location = 0.0, 0.0, 0.0  &\n\
   orientation = 0.0d, 0.0d, 0.0d\n\
!\n\
part create point_mass mass_properties  &\n\
   point_mass_name = .CooperativeControls.POINT_MASS_'+str(Counter)+ ' &\n\
   mass = '+str(Mass)+'  &\n\
   center_of_mass_marker = cm\n')

        
        AdamsID=AdamsID+1
    # If the nodes are on the ground z=0 we fix them
        if line[2]=='0':
            
        #First Create the marker on the ground
            Out.write('!\n\
! ****** Markers for current part ******\n\
!\n\
marker create  &\n\
   marker_name = .CooperativeControls.ground.M_'+str(Counter)+ '  &\n\
   adams_id = '+str(AdamsID)+'  &\n\
   location = 0.0, 0.0, 0.0  &\n\
   orientation = 0.0d, 0.0d, 0.0d\n\
!\n')
            AdamsID=AdamsID+1
        #Now create the actual joint
            Out.write('!\n\
!----------------------------------- Joints -----------------------------------!\n\
!\n\
!\n\
constraint create joint spherical  &\n\
   joint_name = .CooperativeControls.GrndJoint_'+str(Counter)+ '  &\n\
   adams_id = '+str(AdamsID)+'  &\n\
   i_marker_name = .CooperativeControls.POINT_MASS_'+str(Counter)+ '.cm  &\n\
   j_marker_name = .CooperativeControls.ground.M_'+str(Counter)+ '\n\
!\n\
constraint attributes  &\n\
   constraint_name = .CooperativeControls.GrndJoint_'+str(Counter)+ '  &\n\
   name_visibility = off\n')
        
        
        AdamsID=AdamsID+1
        Counter=Counter+1


Out.close()
# ---------------------------------------------------------------------------------
# For loop two Inserting elements, that is the springs between the point masses
#
# ---------------------------------------------------------------------------------

Out2=open(Output,'a')
SpringCounter=1 #Total number of springs created 
TotalSpring=0
TotalForce=15 #Start at 15 as there should be already 14 forces in the model
with open('SpringsNew.csv', 'rb') as f:
    
    
    # Elements define how the point nodes are connected, this means that the
    # elements file defines where the springs of the model are located
    
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    
    
    for row in reader:


        imarker=row[0]
        jmarker=row[1]
        Stiffness=row[2]

        # Check if the spring is on the boundary, if so don't write the spring
        SpringBoundary=0
        
        with open('FrontNew.csv','rb') as fr:
            Frontiere = csv.reader(fr, delimiter=',', quoting=csv.QUOTE_NONE)
            for Frontrow in Frontiere:
                
                if imarker==Frontrow[0] and jmarker==Frontrow[1]:
                    SpringBoundary=1
                    
                    
                   
            
        # For each row 3 springs are defined:
        # i marker is row[0] with the jmarker as row[1], row[2] or row[3]

        # If it is a boundary spring we replace it with a force that can be suppressed by the cutting force
        if (SpringBoundary==1):
            TotalForce=TotalForce+1 #Adding a Force
            Out2.write('!\n\
!----------------------------------- Forces -----------------------------------!\n\
!\n\
!\n\
force create direct single_component_force  &\n\
   single_component_force_name = .CooperativeControls.SFORCE_'+str(TotalForce)+'  &\n\
   adams_id = '+str(AdamsID)+'  &\n\
   type_of_freedom = translational  &\n\
   i_marker_name = .CooperativeControls.POINT_MASS_'+str(imarker)+'.cm  &\n\
   j_marker_name = .CooperativeControls.POINT_MASS_'+str(jmarker)+'.cm  &\n\
   action_only = off  &\n\
   function = ""\n\
!\n\
!\n\
defaults coordinate_system  &\n\
   default_coordinate_system = .CooperativeControls.ground\n\
!\n')
            AdamsID=AdamsID+1
            Out2.write('!\n\
geometry create shape force  &\n\
   force_name = .CooperativeControls.SFORCE_'+str(TotalForce)+'_force_graphic_'+str(TotalForce)+'  &\n\
   adams_id = '+str(AdamsID)+'  &\n\
   force_element_name = .CooperativeControls.SFORCE_'+str(TotalForce)+'  &\n\
   applied_at_marker_name = .CooperativeControls.POINT_MASS_'+str(imarker)+'.cm\n\
!\n\
!---------------------------- Function definitions ----------------------------!\n\
!\n\
!\n\
force modify direct single_component_force  &\n\
   single_component_force_name = .CooperativeControls.SFORCE_'+str(TotalForce)+'  &\n\
   function = "'+str(Force)+'*(0.005-DM( .CooperativeControls.POINT_MASS_'+str(imarker)+'.cm,.CooperativeControls.POINT_MASS_'+str(jmarker)+'.cm))"\n\
!!')
            AdamsID=AdamsID+1
        else:
            TotalSpring=TotalSpring+1 # Adding a Spring
            Out2.write('! \n\
!----------------------------------- Forces -----------------------------------!\n\
!\n\
!\n\
!-------------------------- Adams/View UDE Instances --------------------------!\n\
!\n\
!\n\
defaults coordinate_system  &\n\
default_coordinate_system = .CooperativeControls.ground\n\
!\n\
undo begin_block suppress = yes\n\
!\n\
ude create instance  &\n\
   instance_name = .CooperativeControls.SPRING_'+str(TotalSpring)+' &\n\
   definition_name = .MDI.Forces.spring  &\n\
   location = 0.0, 0.0, 0.0  &\n\
   orientation = 0.0, 0.0, 0.0\n\
!\n\
ude attributes  &\n\
   instance_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'  &\n\
   color = RED\n\
   !\n')
            Out2.write('!\n\
!-------------------------- Adams/View UDE Instance ---------------------------!\n\
!\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.i_marker  &\n\
   object_value = (.CooperativeControls.POINT_MASS_'+str(imarker)+'.cm)\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.j_marker  &\n\
   object_value = (.CooperativeControls.POINT_MASS_'+str(jmarker)+'.cm)\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.stiffness_mode  &\n\
   string_value = "linear"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.stiffness_coefficient  &\n\
   real_value = ('+str(Stiffness)+'(newton/meter))\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.stiffness_spline  &\n\
   object_value = (NONE)\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.damping_mode  &\n\
   string_value = "linear"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.damping_coefficient  &\n\
   real_value = ('+str(Damping)+'(newton-sec/meter))\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.damping_spline  &\n\
   object_value = (NONE)\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.free_length_mode  &\n\
   string_value = "Design_Length"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.free_length  &\n\
   real_value = 1.0\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.preload  &\n\
   real_value = 0.0\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.i_dynamic_visibility  &\n\
   string_value = "Off"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.j_dynamic_visibility  &\n\
   string_value = "Off"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.spring_visibility  &\n\
   string_value = "Depends"\n\
!\n\
variable modify  &\n\
   variable_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'.damper_visibility  &\n\
   string_value = "never"\n\
!\n\
ude modify instance  &\n\
   instance_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'\n\
!\n\
undo end_block\n\
!\n')
            Out2.write('!-------------------------- Adams/View UDE Instance ---------------------------!\n\
!\n\
!\n\
ude modify instance  &\n\
   instance_name = .CooperativeControls.SPRING_'+str(TotalSpring)+'\n\
!\n')
            

            
            
        SpringCounter=SpringCounter+1
print "Total Springs",TotalSpring
print "Total Forces",TotalForce
print "Total Springs",SpringCounter
Out2.close()        
            














