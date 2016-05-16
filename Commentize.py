
import os 
import tkFileDialog
import time
import fileinput
path = tkFileDialog.askdirectory(initialdir="/", title='Please select a directory')



Notice=('%%C \n\
%----------------------------------------------------------\n\
% Copyright (c) 2012 Philip Long\n\
% Permission is hereby granted, free of charge, to any person obtaining a copy\n\
% of this software and associated documentation files (the "Software"), to deal\n\
% in the Software without restriction, subject to the following conditions:\n\
%\n\
% The above copyright notice and this permission notice shall be included in\n\
% all copies or substantial portions of the Software.\n\
%\n\
% The Software is provided "as is", without\n\
% warranty of any kind.\n\
%---------------------------------------------------------- ')




listing = os.listdir(path) # List all files in folder
Count=0
for infile in listing:
    Count=Count+1
    ParFile=open(path+'/'+str(infile),'r') #Open File to read  one at a time
    
    print "current file is: " + infile

    
    if infile[-2:]==".m": #If it is a matlab file
        print "yes it is a matlab file"
        for line in fileinput.input(infile, inplace=1):
            if line.startswith('%%C'):
                #Already commented
                pass
            else:
                print Notice
