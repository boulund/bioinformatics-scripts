#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Extract sequences from a FASTA file 

from read_fasta import read_fasta
from sys import argv, exit, maxint
import argparse


def parse_args(argv):
    """Parse commandline arguments.
    """

    desc = """Extract sequences from FASTA files. Fredrik Boulund 2015"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", nargs="+",
            help="FASTA file to sample from.")
    parser.add_argument("--maxlength", metavar="M", type=int,
            default=0,
            help="Maximum length of sequences to extract, 0 means no limit [%(default)s]")
    parser.add_argument("--minlength", metavar="m", type=int,
            default=0,
            help="Minimum length of sequences to extract, 0 means no limit [%(default)s].")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILE instead of STDOUT.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def extract_from_fasta(fastafile, maxlength=0, minlength=0):
    """Extract sequences from FASTA.

    Will write to STDOUT if outfile evaluates to False.
    """

    if not maxlength:
        maxlength = maxint

    seqs = []

    for header, seq in read_fasta(fastafile):
        seqlen = len(seq)
        if seqlen >= minlength and seqlen <= maxlength:
            yield (">"+header, seq)


if __name__ == "__main__":
    options = parse_args(argv)
    if options.outfile:
        with open(options.outfile, 'w') as outfile:
            for filename in options.FASTA:
                for seq in extract_from_fasta(filename, options.maxlength, options.minlength):
                    outfile.write('\n'.join(seq)+"\n")
    else:
        for filename in options.FASTA:
            for seq in extract_from_fasta(filename, options.maxlength, options.minlength):
                print '\n'.join(seq)


