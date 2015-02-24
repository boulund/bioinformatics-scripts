#!/usr/bin/env python
# Maps ARDB identifiers to the
# ARGENE00000-variant used in 
# ShotgunFunctionalizeR by adding
# the SFR-tag to the identifier line

from sys import argv

# File containing the gene mappings
mappings_file = '/home/boulund/ARDB/improved_ARDB/src/ARGenes_mapping.txt'
# Read the entire file and store each line contaning
# mapping information into a nestled list for
# simple searching
mappings_list = []
for line in open(mappings_file):
    mappings_list.append(line.split())

# Open the file given at command line 
# assuming it contains a FASTA-version
# of the sequences to be 'mapped'.
try:
    ardbfile = open(argv[1])
    for line in ardbfile:
        if line.startswith(">"):
            splitline = line.split(" ")
            for genefamily in mappings_list:
                if splitline[0][1:] in genefamily[2]:
                    print ''.join([line[0],",",genefamily[0],", ",line[1:]]),
                    break #could be used to prevent unfortunate double-mappings
        else:
            print line,
except IndexError:
    print "IndexError"

