#!/usr/bin/python
# Retrieves sequences from a fasta file and outputs them
# to stdout for redirection to file

from fluff import retrieve_sequences_from_fasta
from sys import argv, exit

if len(argv) < 2:
    print "Usage: script.py seqid1.. fastafile\nImportant that fastafile is last!"
    print "If first argument is a single character, l, sequences will be printed on ONE line"
    exit(1)


filename = argv[-1] # fasta file is last file in argv
seqids = argv[1:-1] # all but last item in argv are seqids

if seqids[0]=="l":
    seqids = seqids[1:]
    ONELINE = True
else:
    ONELINE = False


try:
    sequences = retrieve_sequences_from_fasta(filename,seqids)
    for sequence in sequences:
        if ONELINE:
            seq = sequence.split("\n")
            print seq[0]
            print ''.join(seq[1:])
        else:
            print sequence
except ValueError:
    print "No sequences found!"
