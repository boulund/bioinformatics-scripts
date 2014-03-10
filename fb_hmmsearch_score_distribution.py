#!/usr/bin/env python
# Compare scores between different source databases 
# to the qnr model.

from sys import argv, exit
from fluff import parse_hmmsearch_output as parsehmm

# Go through the input files and output scores into files,
# Then use R to plot the scores (not included in script)

if len(argv) < 2:
    print "usage: script.py hmmsearchfile(s)..."
    exit()

for filename in argv[1:]:
    parseoutput = parsehmm(filename)
    scoretuple, dbpath = parseoutput
    seqscores, domscores, ids = zip(*scoretuple)
    with open(filename+".scores",'w') as outfile:
        for score in seqscores:
            outfile.write(score+'\n')

