#!/usr/bin/env python
# Take gzipped fastq-files and change to
# fasta before gzipping them again.

from os import system
from sys import argv

for file in argv[1:]:
    print "Gunzipping",file
    system('gunzip '+file)
    print "FASTQ2FASTA",file[:-3]
    system('fb_fastq2fasta.py '+file[:-3])
    print "Gzipping",file[:-3]+'.fasta'
    system('gzip '+file[:-3]+'.fasta')
    print "Gzipping",file[:-3]
    system('gzip '+file[:-3])
    print "Moving",file[:-3]+'.fasta.gz'
    system('mv '+file[:-3]+'.fasta.gz ..')
    print "---------------" 
