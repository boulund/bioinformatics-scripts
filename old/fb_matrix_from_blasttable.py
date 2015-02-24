#!/usr/bin/env python
# Fredrik Boulund 2012-07-05 (c)
# Parses blast table output 6 to produce a neat
# table with all-vs-all similarity scores from
# the alignments.

from sys import argv, exit
import os


def runBLASTP(fastafile):
    """
    Runs BLASTP (external program)
    """
    
    formatdbcall = "formatdb -i "+fastafile 
    blastpcall = "blastp -query "+fastafile+" -db "+fastafile+" -outfmt 6 >"+fastafile+".blasttable"
    os.system(formatdbcall)
    os.system(blastpcall)


def printTable(filename):
    """
    Takes a BLASTTABLE (6) filename and outputs all-vs-all similarity matrix to stdout
    """
    # Dictionary to hold the information
    data = {}
    with open(filename) as blasttable:
        for line in blasttable:
            query, subject, identity = line.split()[0:3]
            try:
                data[query][subject] = identity
            except KeyError:
                data[query] = {subject: identity}

    sortedkeys = data.keys()
    sortedkeys.sort()
    for query in sortedkeys:
        print "\t"+query,
    print ""
    for query in sortedkeys:
        print query,
        for subject in sortedkeys:
            try:
                print "\t"+data[query][subject],
            except KeyError:
                print "\t0.00",
        print ""



if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: script.py FASTAFILE"
        print "Makes an ALL-vs-ALL comparison of sequences in FASTAFILE "\
              "using BLASTP and prints it to stdout.\n"\
              "It automatically creates a BLAST database using formatdb."
        exit()
    else:
        runBLASTP(argv[1])
        printTable(argv[1]+".blasttable")

