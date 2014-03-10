#!/usr/bin/env python

import re
from sys import argv, exit

if len(argv)<2:
    print "Usage: script.py file.hmm..."
    exit()


regex = re.compile(r'Target sequences:\s+(\d+)\s+\((\d+) residues\)')

residues = 0
sequences = 0

hmmfiles = argv[1:]
for hmmfile in hmmfiles:
    for line in open(hmmfile):
        hit =  re.search(regex,line)
        if hit is not None:
            sequences += int(hit.group(1))
            residues += int(hit.group(2))


print "Sequences:",sequences,"\nResidues:",residues
