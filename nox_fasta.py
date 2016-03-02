#!/usr/bin/env python3.5
# Remove sequences containing X from FASTA file
# Fredrik Boulund 2016

from read_fasta import read_fasta
from sys import argv, exit, stdout
import argparse


def parse_args(argv):
    """
    Parse commandline arguments.
    """

    desc = """Remove sequences containing X from FASTA files. Fredrik Boulund 2016"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", 
            help="FASTA file to remove sequences from.")
    parser.add_argument("-r", "--remove", dest="remove", 
            default="Xx",
            help="Remove sequences containing these characters [%(default)s].")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILE instead of STDOUT.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def clean_fasta(fastafile, remove_chars, outfile):
    """
    Remove sequences from FASTA containing any of the characters in remove_chars.

    Will write to STDOUT if outfile evaluates to False.
    """

    charset = set(remove_chars)

    if outfile:
        outhandle = open(outfile, 'w')
    else:
        outhandle = stdout
    
    with outhandle: 
        for header, seq in read_fasta(fastafile):
            if any((char in charset) for char in seq):
                continue
            print(">"+header, file=outhandle)
            print(seq, file=outhandle)


if __name__ == "__main__":
    options = parse_args(argv)
    clean_fasta(options.FASTA, options.remove, options.outfile)
