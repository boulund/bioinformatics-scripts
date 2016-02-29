#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Print sequence lengths and headers

from sys import argv, exit
import os
import fnmatch

if len(argv) < 2:
    print "usage: script.py REFSEQDIR"
    exit()


def find_files(directory, pattern):
    """Generator that yields files by recursively searching a dir with a glob pattern."""
    for root, subfolders, files in os.walk(directory, followlinks=True):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def read_fasta(filename, keep_formatting=True):
    """Read sequence entries from FASTA file
    NOTE: This is a generator, it yields after each completed sequence.
    Usage example:
    for header, seq in read_fasta(filename):
        print ">"+header
        print seq
    """

    with open(filename) as fasta:
        line = fasta.readline().rstrip()
        if not line.startswith(">"):
            raise IOError("Not FASTA format? First line didn't start with '>'")
        if keep_formatting:
            sep = "\n"
        else:
            sep = ""
        first = True
        seqlen = 0
        header = ""
        while fasta:
            if line == "": #EOF
                yield seqlen, header
                break
            elif line.startswith(">") and not first:
                yield seqlen, header
                header = line.split()
                seqlen = 0
            elif line.startswith(">") and first:
                header = line.split()
                first = False
            else:
                seqlen += len(line.rstrip())
            line = fasta.readline()



if __name__ == "__main__":
    seqinfo = []
    for fna in find_files(argv[1], "*.fna"):
        for info in read_fasta(fna, keep_formatting=True):
            seqinfo.append(info)

    seqinfo.sort(key=lambda x: x[0])
    for length, header in seqinfo:
        print "{}\t{}\t{}".format(length, header[0][1:], " ".join(header[1:]))
