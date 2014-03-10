#!/usr/bin/python
# Extracts sequence IDs from the list of hits in
# the output file from 'hmmsearch'.
# Reads two input arguments;
#   First file with results to extract
#   Second an integer (or float with decimal point) for minimum score threshold
#   if threshold not set, default is 0 (i.e. retrieve all hits in file).
# Fredrik Boulund 2010-06-15

from sys import argv, exit
from os import path
import fluff
import re

if len(argv) <= 3 and len(argv) >= 2:
    # Read file given at command line
    filename = path.abspath(argv[1])
    MIN_SCORE = 0 # If no score on command line; defaulting to 0
    if len(argv) == 3:
        try:
            # Set minimum score from second command line argument
            MIN_SCORE = float(argv[2])
        except ValueError:
            print "ERROR: Second argument must be an integer or float"
            exit(2)
else:
    print "Wrong number of command line arguments, need at least one path and not more than two arguments"
    exit(2)

# Parse the hmmsearch output file
try:
    parsed = fluff.parse_hmmsearch_output(filename,MIN_SCORE)
except ValueError:
    print "ERROR: Found no sequences with domain score more than", MIN_SCORE
    exit(1)
except fluff.ParseError, e:
    print e.message
    exit(1)

# Unpack the parsed information
score_id_tuples, dbpath = parsed #Unpack the tuple
scores,dscores,ids = zip(*score_id_tuples) #Unzip the score/id information

seqsnutts = fluff.retrieve_sequences_from_hmmsearch(filename,ids,0.0,dbpath)
