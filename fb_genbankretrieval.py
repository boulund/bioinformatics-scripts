#!/usr/bin/python 
# Retrieves sequences from 
# GenBank using sequence IDs
# given at commandline.

from Bio import Entrez
from sys import argv, stdin,stderr, exit
from os import path

# Check arguments, unless first argument is a dash ("-") 
# assume everything is sequence ids from genbank.
if len(argv) < 2:
    print ("Needs at least one argument:\n"
           "script.py seqid...\n"
           "- can be used to read from stdin")
    exit()


# Set user email address
Entrez.email = "fredrik.boulund@chalmers.se"


# If first argument is a dash,
# read sequence IDs from stdin
if not(argv[1]=="-"):
    seqids = argv[1:]
else:
    seqids = stdin.readlines()

# Retreive sequence for each item in argv
for seqid in seqids:
    seqid.strip()
    #print seqid # troubleshooting
    try:
        handle = Entrez.efetch(db="nucleotide",id=seqid,rettype="fasta")
        sequence = handle.read()
        if "Nothing" in sequence:
            stderr.write(seqid+sequence)
        else:
            print sequence,
    except IOError:
        pass
    except KeyboardInterrupt:
        stderr.write("KeyboardInterrupt, exiting...")
        exit()


