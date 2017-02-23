#!/usr/bin/env python3.5
# Validate sequences in FASTA file
# Fredrik Boulund 2016

from read_fasta import read_fasta
from sys import argv, exit, stdout, stderr
import argparse


def parse_args(argv):
    """
    Parse commandline arguments.
    """

    desc = """Validate sequences in FASTA files. Fredrik Boulund 2017"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", 
            help="FASTA file to remove sequences from.")
    parser.add_argument("-k", "--kind", dest="kind", 
            choices=["n", "nucleotide", "p", "protein"],
            default="nucleotide",
            help="Choose preset [%(default)s].")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write clean output to FILE instead of STDOUT.")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
            default=False,
            help="Print erroneous sequences to STDERR.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def find_errors_in_seq(seq, valid_chars):
    """
    Report errors in seq by showing them in uppercase surrounded by _.
    """
    outchars = []
    incorrect_chars = []
    for char in seq:
        if char.upper() not in valid_chars:
            outchars.append("_")
            outchars.append(char)
            outchars.append("_")
            incorrect_chars.append(char)
        else:
            outchars.append(char.lower())
    return ''.join(outchars), ''.join(incorrect_chars)


def clean_fasta(fastafile, valid_chars, outhandle, verbose):
    """
    Report sequences from FASTA containing any other character than what is in valid_chars.

    Will write to STDOUT if outfile evaluates to False.
    """

    charset = set(valid_chars)

    with outhandle: 
        for header, seq in read_fasta(fastafile):
            if any((char.upper() not in charset) for char in seq):
                errorseq, errorchars = find_errors_in_seq(seq, valid_chars)
                if verbose:
                    print("WARNING: found {} in {}\n{}".format(errorchars, header, errorseq), file=stderr)
                else:
                    print("WARNING: found {} in {}".format(errorchars, header), file=stderr)
                continue
            print(">"+header, file=outhandle)
            print(seq, file=outhandle)


if __name__ == "__main__":
    options = parse_args(argv)

    if options.kind.startswith("n"):
        valid_chars = "ATGC\n"
    else:
        valid_chars = "ACDEFGHIKLMNOPQRSTUVWY\n"

    if options.outfile:
        outhandle = open(outfile, 'w')
    else:
        outhandle = stdout
    
    clean_fasta(options.FASTA, valid_chars, outhandle, options.verbose)
