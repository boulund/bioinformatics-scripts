#!/usr/bin/env python
# Retrieves nucleotide sequences from database with *.cidx file (cdbfasta)
# Uses (obviously) the cdbfasta tools
# Fredrik Boulund 2011-11-01

from sys import argv, exit
from os import path
import re, shlex, subprocess

if len(argv)<2:
    print "Usage: script.py file"
    print "Takes a file with sequence headers (cidx-headers) and retrieves the"
    print "corresponding nucleotide sequences from the assumed existing *.nfa"
    print "file in the directory given on the first line of the input file"
    print "The expected form of sequence headers is:"
    print "[sourcefile stem]_[source header name]  e.g."
    print "SRR006906_SRR006906.178661"
    exit()

# Regexp to match the sequence headers and parse them into assumed nucleotide
# FASTA (cidx) headers

regex_head = re.compile(r'^(\w+)\_(.+)$')

file = open(argv[1])

dbdir = path.abspath(file.readline().strip())

for line in file:
    #print line,
    hit = re.search(regex_head,line)
    if hit is not None:
        #print hit.group(1), hit.group(2)

        stem = path.abspath(''.join([dbdir, "/", hit.group(1), ".nfa.cidx"]))

        if path.isfile(stem):
            #print stem
            cdbyank_call = ''.join(["cdbyank ", stem, " -a ", hit.group(2).strip()])
            cdbyank_args = shlex.split(cdbyank_call)
            # Spawn the cdbyank process and retrieve stdout
            stdout, stderr = subprocess.Popen(cdbyank_args,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate()

            if stderr:
                print "error", stderr
            else:
                print stdout
