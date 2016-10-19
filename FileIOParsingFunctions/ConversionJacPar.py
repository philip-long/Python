# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 08:56:41 2012
This files changes the parameters of SYMORO to parameters I can use directly in Matlab, this also
coverts the .jac file into a usable matlab function
@author: user
"""

import os 
import tkFileDialog
import time  
path = tkFileDialog.askdirectory(initialdir="/", title='Please select a directory')
#path='D:/Mes documents/functions/PythonTests/Params'
    # test
listing = os.listdir(path) # List all files in folder
Count=0
for infile in listing:
    Count=Count+1
    ParFile=open(path+'/'+str(infile),'r') #Open File to read  one at a time
    
    print "current file is: " + infile

    
    if infile[-4:]==".par": #If it is a parameter file
       # Re=open('D:/Mes documents/functions/Python Funcs/PythonOutputs/'+str(infile[:-4])+'.txt','w') #Open replacement file of parameters
        Re=open(path+'/'+str(infile[:-4])+'.txt','w') #Open replacement file of parameters 
        for line in ParFile:      #Check each line
            
            L=line.replace("}","];") #Replace Matematica Brackets by Matlab 
            L=L.replace("(*","%") #Replace comments by matlab comments          
            L=L.replace("*)"," ") #Replace comments by matlab comments
            L=L.replace("Pi","pi") #Replace Pi by pi
            L=L.replace("{\n","[") #Replace Matematica Brackets by Matlab 
            Re.write(L.replace("  ",""))

            
    elif infile[-4:]==".jac":#If it is a Jacobian file
       # Re=open('D:/Mes documents/functions/Python Funcs/PythonOutputs/'+str(infile[:-4])+'.txt','w') #Open replacement file of parameters 
        Re=open(path+'/'+str(infile[:-4])+'.txt','w') #Open replacement file of parameters 
        fname='function J='+infile[:-4]+'(u)'#Specially constructed string characters to search for
        S1=' '+'+'+' '+'\n' 
        S2=' '+'-'+' '+'\n'
        S3='='+' '+'0'+'\n'
        S4='='+' '+'1'+'\n'
        
        print fname
        Uncomment=0 #Flag that comments out the header matter       
        for line in ParFile:#Check each line
            
            L=line
            if "----------------------------------" in L:
                Uncomment=1
                print "Uncommented"
                L=L.replace("----------------------------------",fname) #Function name
                        
            L=L.replace(")\n",");\n") #Semi Colons
            L=L.replace(")\n",");\n") #Semi Colons        
            L=L.replace(S3,"=0;\n") #Semi Colons
            L=L.replace(S4,"=1;\n") #Semi Colons  
            
            L=L.replace(S1,"+...\n") #Replace Lines breaks that Matlab can't see +
            L=L.replace(S2,"-...\n") #Replace Lines breaks that Matlab can't see -
            
            L=L.replace("{\n","[") #Replace Matematica Brackets by Matlab 
            L=L.replace("}","];") #Replace Matematica Brackets by Matlab 
            
            
            L=L.replace("(*","%") #Replace comments by matlab comments
            L=L.replace("*)"," ") #Replace comments by matlab comments

            L=L.replace("Pi","pi") #Replace Pi by pi
            L=L.replace("Sin","sin") #Replace Sin by sin
            L=L.replace("Cos","cos") #Replace Cos by cos
            
            
            if "I" in L and "|" in L  and "L" in L: #Exits at the end
                break
            elif Uncomment==1:  #Comments out all the begininng part
                Re.write(L)
            else: 
                Re.write('%'+L)
            
            
            
