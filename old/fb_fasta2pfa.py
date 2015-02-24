#!/usr/bin/env python
# Convert fasta to protein fasta
# using emboss

from sys import argv, exit
from os import system

if len(argv)<2: 
    print ("Usage: script.py file.fasta ...\n")


for filename in argv[1:]:
    # Construct the call to transeq
    transeqcall = "transeq -sequence "+filename+" -frame 6 -table 11 -outseq "+filename+".pfa"
    print transeqcall
    system(transeqcall)
