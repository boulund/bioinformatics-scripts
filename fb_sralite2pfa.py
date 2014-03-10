#!/usr/bin/env python
# Converts sra.lite to protein fasta
# using sra-tools and emboss

from sys import argv, exit
from os import system

if len(argv)<2:
    print ("Usage: script.py files.sra.lite ...\n"
           "Takes sra.lite files and converts to protein fasta (pfa)")
    exit()

for filename in argv[1:]:
    # Construct the call to fastq-dump
    fastqdumpcall = "fastq-dump "+filename
    print fastqdumpcall
    system(fastqdumpcall)
    

    # Change filename-variable to reflect 'new' file
    filename = filename[0:-9]
    # Construct the call to seqret (emboss)
    seqretcall = "seqret -sequence "+filename+".fastq -outseq "+filename+".fasta"
    print seqretcall
    system(seqretcall)

    # Construct the call to transeq (emboss)
    transeqcall = "transeq -sequence "+filename+".fasta -frame 6 -table 11 -outseq "+filename+".pfa"
    print transeqcall
    system(transeqcall)
