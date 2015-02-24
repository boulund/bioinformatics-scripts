#!/usr/bin/env python
# Compute the average runtime for
#Vmatch with different settings
#on different files

from sys import argv
import os
import re


""" Open the tid.*.* and vmatchoutput.*.* files and read the time
    taken for each run. Then present some general statistics..."""

regextid = re.compile(r'real\s+(.+)') # Matches e.g. 'real 14512.44'
regexline = re.compile(r'^# args=(.+)') # Matches command lines from the vmatch output
list_of_lines = []
prevline = ''
list_of_times = []
for filename in argv[1:]:
    curtimes = 0
    count = 0
    if "tid" in filename:
        # Open the tid-file and store
        # all times in a list.
        #print "Opening",filename
        file = open(filename,'r')
        curtimes = [filename]
        for line in file:
            hit = re.search(regextid,line)
            if hit is not None:
                #print "Time:", hit.group(1)
                curtimes.append(float(hit.group(1)))
        list_of_times.append(curtimes) 

    elif "vmatch" in filename:
        # Open the file and extract all commandlines in order
        #print "Opening",filename
        file = open(filename,'r')
        for line in file:
            hit = re.match(regexline,line)
            if hit is not None:
                #print "Command line:",hit.group(1)
                curline = hit.group(1)
                if curline != prevline:
                    list_of_lines.append(curline)
                    prevline = curline


info = zip(list_of_times,list_of_lines)

for things in info:
    times, line = things
    print line

    # Average
    avg = sum(times[1:])/len(times[1:])
    # Standard deviation
    sdsq = sum([(i - avg) ** 2 for i in times[1:]])
    stdev = (sdsq / (len(times[1:]) - 0.999999999999999)) ** .5 #orka importera sqrt!

    print "Average: %3.3fm (%3.3fh)" % (float(avg/60), float(avg/3600)) #hours
    print "Stdev  : %3.3fm" % float(stdev/60) #minutes
