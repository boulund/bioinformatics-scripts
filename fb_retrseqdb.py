#!/usr/bin/python
# Extracts sequence IDs from the list of hits in
# the output file from 'hmmsearch' and retrieves
# them from their database as mentioned in the 
# hmmsearch output file.
# Reads two input arguments;
#   First file with results to extract
#   Second an integer (or float with decimal point) for minimum score threshold
#   if threshold not set, default is 0 (i.e. retrieve all hits in file).
# Fredrik Boulund 2010-06-17

from sys import argv, exit
from os import path
import fluff
import re

if len(argv) <= 3 and len(argv) >= 2:
    # Read file given at command line
    try:
        file = open(path.abspath(argv[1]),"r")
    except IOError:
        print "Something wrong with path:", argv[1]
        exit(2)
    MIN_SCORE = 0 # If no score on command line; defaulting to 0
    if len(argv) == 3:
        # Set minimum score from second command line argument
        MIN_SCORE = float(argv[2])
else:
    print "Wrong number of command line arguments,\nusage: script.py HMMSEARCHOUTPUTFILE min_score"
    exit(2)

# Parse the hmmsearch output file
try:
    parsed = fluff.parse_hmmsearch_output(file,MIN_SCORE)
except ValueError:
    print "ERROR: Found no sequences with domain score more than", MIN_SCORE
    exit(1)

# Unpack the parsed information
score_id_tuples, dbpath = parsed #Unpack the tuple
scores,dscores,ids = zip(*score_id_tuples) #Unzip the score/id information

# Retrieve sequences from database
try:
    sequences = fluff.retrieve_sequences_from_db(dbpath,ids)
except fluff.PathError, (error):
    print error.message,"\n", dbpath #"ERROR: The path specified in the hmmsearch output is not valid."
    exit(1)
except ValueError:
    print "ERROR: No sequences found in the database!"
    exit(1)

for sequence in sequences: print sequence,
