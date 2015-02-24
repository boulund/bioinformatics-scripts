#!/usr/bin/env python
# Fredrik Boulund 2015
# Add sequence length to the end of FASTA headers.

from sys import argv, exit
from read_fasta import read_fasta

if len(argv) < 2:
    print "usage: script.py FILE > output.fasta"
    exit()

for header, seq in read_fasta(argv[1]):
    hsplit = header.split()
    print ">"+hsplit[0]+"_"+str(len(seq))+' '.join(hsplit[1:])
    print seq
