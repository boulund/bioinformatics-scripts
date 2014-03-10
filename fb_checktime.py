#!/usr/bin/env python
# Compute the average runtime for
# Vmatch with different settings
# on different files

from sys import argv
import os
import re


""" Open the tid.* and vmatchoutput.* files and read the time
    taken for each run. Also compute the average time..."""

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
                break


info = zip(list_of_times,list_of_lines)


timesum = 0
for things in info:
    times, line = things
    timesum = timesum+times[1]
    print line
    print "Time: %3.3fm" % float(times[1]/60) #minutes

print "\nAverage: %3.3fm" % float(timesum/(len(list_of_times)*60))
