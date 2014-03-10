#!/usr/bin/env python
# Sends input from stdin (pipe) to blastp query

from sys import stdin
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

print "Ready to send data from stdin to ncbi blast:"
sequence = stdin.read()
print sequence
print "Submitting..."
handle = NCBIWWW.qblast('blastp','nr',sequence) #,format_type="text")

blast_record = NCBIXML.read(handle)
for alignment in blast_record.alignments:
    print alignment
