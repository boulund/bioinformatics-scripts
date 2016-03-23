#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Print sequence lengths and headers

from sys import argv, exit
import os
import fnmatch

from read_fasta import read_fasta, read_fastq

if len(argv) < 2:
    print "usage: script.py FILE [...]"
    exit()

if __name__ == "__main__":
    for filename in argv[1:]:
        if filename.endswith((".fasta", ".fa", ".fna", ".pfa")):
            file_is_fasta = True
        elif filename.endswith((".fastq", ".fq")):
            file_is_fasta = False
        else:
            print("WARNING: Unknown filetype of {}".format(filename))
            continue
        if file_is_fasta:
            for header, seq in read_fasta(filename):
                print("{}\t{}".format(len(seq), header))
        else:
            for header, seq, _, _ in read_fastq(filename):
                print("{}\t{}".format(len(seq), header[1:]))
