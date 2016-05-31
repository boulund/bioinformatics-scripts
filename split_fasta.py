#!/usr/bin/env python3.5
# Fredrik Boulund 2016
# Split a FASTA file based on number of sequences

from read_fasta import read_fasta
from sys import argv, exit
from math import ceil
from collections import deque
import argparse

def parse_args(argv):
    """
    Parse commandline arguments.
    """

    desc = """Split FASTA files. Fredrik Boulund 2016"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", 
            help="FASTA file to split.")
    parser.add_argument("-n", dest="n", metavar="N", required=True, type=int,
            help="Number of file to split to [%(default)s].")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILEnn instead of STDOUT.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def main(options):
    """
    Main function.
    """
    sequences = deque(read_fasta(options.FASTA))

    if options.outfile:
        outfilename = options.outfile
    else:
        outfilename = options.FASTA

    outfiles = ["{}{:02d}".format(outfilename, nn) for nn in range(1, options.n+1)]

    seqs_per_file = ceil(len(sequences) / options.n)
    print("Splitting {filename} into {n} files with (at most) {seqs} sequences per file".format(
            filename=options.FASTA, n=options.n, seqs=ceil(seqs_per_file)))

    for outfile in outfiles:
        with open(outfile, "w") as f:
            for n in range(0, seqs_per_file):
                try:
                    header, seq = sequences.popleft()
                except IndexError:
                    # The deque is empty
                    break
                print(">"+header, file=f)
                print(seq, file=f)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)
