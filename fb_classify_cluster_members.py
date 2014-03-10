#!/usr/bin/env python
# Classify cluster members according to
# fasta file of reference sequences.

from sys import argv, exit
from FB_functions import read_fasta
import re


if len(argv)<2:
    print "usage: script.py cluster.fasta..."
    exit()

refseqs = read_fasta("/home/boulund/qnr-search_project/qnrsequences/pmqr.pfa")


# Compile a regex to find the Qnr-tag of the reference sequences
qnrname_regex = re.compile(r'(Qnr\w\d*)')

for file in argv[1:]:
    #print "\n"+file+"\n"
    outfile = open(file+".classified","w")
    cluster = read_fasta(file)
    for seq in cluster:
        success = False
        for refseq in refseqs:
            qnrname = re.search(qnrname_regex,refseq[0])
            if qnrname is not None:
                if seq[1] in refseq[1]:
                    success = True
                    outfile.write(">-"+qnrname.group(0)+"-"+seq[0][1:]+"\n")
                    outfile.write(seq[1]+"\n")
                    print ">-"+qnrname.group(0)+"-"+seq[0][1:]
                    #print seq[1]
        if not success:
            outfile.write('\n'.join(seq)+"\n")
            #print '\n'.join([seq[0],seq[1]])
