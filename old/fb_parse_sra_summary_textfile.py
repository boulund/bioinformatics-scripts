#!/usr/bin/python
# Parses sra summary text files for 
# sequence run ids (e.g. SRR006232)

from sys import argv, exit
import re


if len(argv)<2:
    print "Usage: script.py sra_textfile"
    exit()


# Regex for matching sequence run ids
regex = re.compile(r'\d+:\s((\w\w\w)(\d\d\d)(\d\d\d))')

for line in open(argv[1]):
    if line.startswith("Run"):
        hit = re.search(regex,line)
        if hit is not None:
            print hit.group(1)



