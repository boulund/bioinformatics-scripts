#!/usr/bin/env python2.7
# Fredrik Boulund 2015
# Extract sequences from a FASTA file 

from read_fasta import read_fasta
from sys import argv, exit, maxint
import argparse
import re


def parse_args(argv):
    """Parse commandline arguments.
    """

    desc = """Extract sequences from FASTA files. Fredrik Boulund 2015"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", nargs="+",
            help="FASTA file(s) to sample from.")
    parser.add_argument("-M", "--maxlength", metavar="M", type=int,
            default=0,
            help="Maximum length of sequences to extract, 0 means no limit [%(default)s]")
    parser.add_argument("-m", "--minlength", metavar="m", type=int,
            default=0,
            help="Minimum length of sequences to extract, 0 means no limit [%(default)s].")
    parser.add_argument("-o", "--outfile", metavar="FILE", dest="outfile",
            default="",
            help="Write output to FILE instead of STDOUT.")
    parser.add_argument("-r", "--regex", metavar="'REGEX'", dest="regex",
            default="",
            help="Extract sequences with header that match REGEX.")
    parser.add_argument("-R", "--regex-file", metavar="FILE", dest="regex_file",
            default="",
            help="Extract sequences with header matching any of multiple regexes on separate lines in FILE.")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def extract_from_fasta(fastafile, maxlength=0, minlength=0, regexes=""):
    """Extract sequences from FASTA.

    Will write to STDOUT if outfile evaluates to False.
    """


    seqs = []

    for header, seq in read_fasta(fastafile):
        if regexes:
            hits = [re.match(rex, header) for rex in compiled_regexes]
            if not any(hits):
                continue
        seqlen = len(seq)
        if seqlen >= minlength and seqlen <= maxlength:
            yield (">"+header, seq)


if __name__ == "__main__":
    options = parse_args(argv)

    if not options.maxlength:
        maxlength = maxint
    else:
        maxlength = options.maxlength

    if options.regex:
        compiled_regexes = [re.compile(options.regex)]
    elif options.regex_file:
        with open(options.regex_file) as regexes:
            compiled_regexes = [re.compile(rex.strip()) for rex in regexes.readlines()]

    extraction_generators = (extract_from_fasta(filename, maxlength, options.minlength, compiled_regexes) for filename in options.FASTA)

    if options.outfile:
        with open(options.outfile, 'w') as outfile:
            for extraction_generator in extraction_generators:
                for seq in extraction_generator:
                    outfile.write('\n'.join(seq)+"\n")
    else:
        for extraction_generator in extraction_generators:
            for seq in extraction_generator:
                print '\n'.join(seq)
