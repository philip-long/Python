# -*- coding: utf-8 -*-
import lxml.etree as ltr
import os


def main(): 
    ROOT = ltr.Element("launch") 
    indir = './dynamic_maps/'     
    for filename in os.listdir(indir):
        if(filename.startswith("calibration_config")):
            ROSPARAM2=ltr.SubElement(ROOT,"rosparam",{"command":"load","file":"$(find ur_package)/config/dynamic_maps/"+filename})
        for i in range(5):           
                 sensor=i
                 sensor_name="map_"+str(i)
                 laser="laser"
                 if(i!=0): #Due to inconsistent naming convention Grrrrrrhh
                     laser=laser+"_"+str(i+1)
                 
                 if(filename.startswith(sensor_name) and filename.endswith(".yaml")):
                     path="$(find ur_package)/config/dynamic_maps/"+filename
                     NODE= ltr.SubElement(ROOT,"node", name=filename[0:-len(".yaml")],
                                          pkg="map_server",
                                          type="map_server",
                                          args=path) 
                     ROSPARAM=ltr.SubElement(NODE,"rosparam")                                          
                     FRAME=ltr.SubElement(ROSPARAM,"frame_id",delete=laser+"delete")                                          
                     REMAP=ltr.SubElement(NODE,"remap",{"from":"/map","to":filename[0:-len(".yaml")]})

                     

    
    
    string=ltr.tostring(ROOT, pretty_print=True,xml_declaration=True)     
#    print "-----------------------------------------------------"    
#    print string
    string=string.replace("<frame_id delete=","frame_id: ")
    string=string.replace("delete\"/>","\"")
    print string
    map_launcher = open("../launch/dynamic_map.launch", "w")
    map_launcher.write(string);

if __name__ == '__main__': main()
    
