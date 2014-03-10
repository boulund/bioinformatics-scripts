#!/usr/bin/env python
# Extract parts of multiple alignment in FASTA format.
# Fredrik Boulund 2011-06-23

from sys import argv, exit
from os.path import isfile
from FB_functions import read_fasta

if len(argv) < 4:
    print "Usage: script.py source.fasta fromPos toPos"
    print "Example:\nfb_extract_parts_of_alignment.py sequences.fasta 10 250\n"
    print "Position starts at 1 and goes to sequence length"
    print "Output is on stdout"
    exit()

# Open the source FASTA file and read it
if isfile(argv[1]):
    src_alignment = read_fasta(argv[1])

# Read the starting and ending positions to extract
lowerbound = int(argv[2])
upperbound = int(argv[3])

# Check if fromPos and toPos are valid
if lowerbound<1 or lowerbound>len(src_alignment[0][1])-1:
    print "Invalid fromPos", lowerbound
    exit()
elif upperbound<lowerbound+1 or upperbound>len(src_alignment[0][1]):
    print "Invalid toPos", upperbound
    exit()

# For each sequence, output everything between FROMPOS to TOPOS
for seqid, seq in src_alignment:
    print seqid
    # Extract parts of the sequence, adjust for python indexing
    print seq[lowerbound-1:upperbound-1]

