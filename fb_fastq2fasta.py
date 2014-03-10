#!/usr/bin/python
# Takes any number of input FASTQ files and converts them
# to FASTA. It uses the seqret program from EMBOSS and 
# expects this to be available on PATH.
# Fredrik Boulund 2011-03-24
from sys import argv
from os import system

if len(argv) < 2:
    print "Usage: script.py infiles..."
else:
    files = argv[1:]
    for file in files:
        print file
        seqret_call = "seqret -sformat fastq-sanger -sequence "+file+" -osformat fasta -outseq "+file+".fasta"
        system(seqret_call)
