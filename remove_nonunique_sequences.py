#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Remove non-unique sequences from FASTA

from sys import argv, exit

from read_fasta import read_fasta


if len(argv) < 2:
    print "usage: script.py FILE"
    exit()


seen_seqs = set()
for header, seq in read_fasta(argv[1]):
    if seq not in seen_seqs:
        seen_seqs.add(seq)
        print ">"+header
        print seq
    
