#!/usr/bin/env python
# Accepts any number of input files on command line
# and runs indexfasta.sh on them

from sys import argv, exit
from os import system

if len(argv) < 2:
    print "Usage: script.py file.pfa file2.pfa ..."
    exit()

for item in argv[1:]:
    call = "indexfasta.sh "+item
    system(call)
