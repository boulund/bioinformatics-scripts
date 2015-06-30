#!/usr/bin/env python
# Reformat fasta files.

from sys import argv, exit
from FB_functions import read_fasta, format_fasta

if len(argv) < 2:
    print "usage: script.py file.fasta 70"
    print "enter an integer to limit the rowlength of the output sequences"
    exit()

try:
    if argv[2] > 1:
        sequences = format_fasta(read_fasta(argv[1]),argv[2])
        for seq in sequences:
            print seq,
except IndexError:
    sequences = format_fasta(read_fasta(argv[1]),70)
    for seq in sequences:
        print seq
