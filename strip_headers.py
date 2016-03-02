#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Strip FASTA headers by removing everything after first space

from sys import argv, exit

if len(argv) < 2:
    print "usage: strip_headers.py FILE"
    print "Writes to STDOUT, a single '-' takes input from STDIN instead of FILE."
    exit()

if argv[1] == "-":
    from sys import stdin
    source = stdin
else:
    source = open(argv[1])

for line in source:
    if line.startswith(">"):
        print line.split()[0]
    else:
        print line,
