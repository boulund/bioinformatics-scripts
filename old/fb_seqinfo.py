#!/usr/bin/python
# Fredrik Boulund 2012
# Count sequence length average
# and max and min from loooong 
# lists produced by infoseq (EMBOSS)
# infoseq -only -length -outfile OUT INFILE


from os import path, system
from sys import argv, exit



if len(argv)<2:
    print "Usage: script.py input.fasta"
    print """Count sequence length average
and max and min from loooong
lists produced by infoseq (EMBOSS)
It calls infoseq on its own, just supply it with sequence filenames"""
    exit()


# go through each sequence file and produce an infoseq output file to parse
for filename in argv[1:]:
    infoseq_call = "infoseq -only -length -outfile "+filename+".seqinfo "+filename
    system(infoseq_call)


    file = open(filename+".seqinfo",'r')

    max = 0 # a smaller number than anticipated longest sequence
    min = 1e1337 # a larger number than anticipated shortest sequence
    long_list = []
    for line in file:
        try:
            number = int(line)
            if number > max:
                max = number
            elif number < min:
                min = number
            long_list.append(number)
        except ValueError:
            pass # i.e. could not convert to integer

#compute true average by dividing by count
try:
    average = sum(long_list) / len(long_list)
    stdev = (sum([(x-average)**2 for x in long_list])/len(long_list))**0.5 #orka importera sqrt
    print "Min seq length:", min
    print "Max seq length:", max
    print "Avg seq length:", average
    print "Standard dev. :", stdev
except ZeroDivisionError:
    print ("Divide by zero, did you use -only -length option?"+
           "\nThis occurs when no lengths could be parsed")
