#!/usr/bin/env python
# Count number of sequences in fasta file

from sys import argv, exit

# Output some usage information
if len(argv) < 2:
    print "usage: script.py file.fasta"
    exit()

# Stream through the file and count occurences of fasta file header >
count = 0
with open(argv[1]) as fastafile:
    for line in fastafile:
        if line.startswith(">"):
            count += 1
# Output the count
print count
