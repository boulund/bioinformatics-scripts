#!/usr/bin/env python
# Remove sequences shorter than

from sys import argv, exit
from FB_functions import read_fasta

if len(argv) < 3:
    print "usage: script.py seqfile.fasta 10"
    print "removes sequences shorter than 10 nucleotides/amino acids"
    exit()

sequences = read_fasta(argv[1])

for sequence in sequences:
    if len(sequence[1]) > int(argv[2]):
        print sequence[0]+"\n"+sequence[1]

