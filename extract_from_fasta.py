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
    parser.add_argument("-b", "--blacklist", metavar="FILE", dest="blacklist",
            default="",
            help="Do not write sequences included in the blacklist FILE. One FASTA header per line.")
    parser.add_argument("-v", "--invert", action="store_true", dest="invert",
            default=False,
            help="Invert sequence selection, i.e. write only sequences that DO NOT match criteria [%(default)s]")

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def extract_from_fasta(fastafile, maxlength=0, minlength=0, regexes="", blacklist="", invert=False):
    """
    Extract sequences from FASTA.
    """

    for header, seq in read_fasta(fastafile):
        if invert:
            if blacklist:
                if header in blacklist:
                    continue
            if regexes:
                if any((re.search(rex, header) for rex in regexes)):
                    continue
            seqlen = len(seq)
            if maxlength == maxint:
                if minlength > seqlen:
                    yield (">"+header, seq)
            if minlength == 0:
                if maxlength < seqlen:
                    yield (">"+header, seq)
            if seqlen < minlength or seqlen > maxlength:
                yield (">"+header, seq)
        else:
            if blacklist:
                if header not in blacklist:
                    continue
            if regexes:
                if not any((re.search(rex, header) for rex in regexes)):
                    continue
            seqlen = len(seq)
            if minlength <= seqlen <= maxlength:
                yield (">"+header, seq)


def parse_blacklist(blacklist_filename):
    """
    Parse blacklist into set.
    """
    blacklist = set()
    with open(blacklist_filename) as f:
        for line in f:
            if line.startswith(">"):
                blacklist.add(line.strip()[1:])
            else:
                blacklist.add(line.strip())
    return blacklist


def main(options):
    """
    Main function.
    """
    if not options.maxlength:
        maxlength = maxint
    else:
        maxlength = options.maxlength

    if options.blacklist:
        blacklist = parse_blacklist(options.blacklist)
    else:
        blacklist = set()

    if options.regex:
        compiled_regexes = [re.compile(options.regex)]
    elif options.regex_file:
        with open(options.regex_file) as regexes:
            compiled_regexes = [re.compile(rex.strip()) for rex in regexes.readlines()]
    else:
        compiled_regexes = ""

    extraction_generators = (extract_from_fasta(filename, 
                                                maxlength=maxlength,
                                                minlength=options.minlength, 
                                                regexes=compiled_regexes,
                                                blacklist=blacklist,
                                                invert=options.invert) for filename in options.FASTA)

    if options.outfile:
        with open(options.outfile, 'w') as outfile:
            for extraction_generator in extraction_generators:
                for seq in extraction_generator:
                    outfile.write('\n'.join(seq)+"\n")
    else:
        for extraction_generator in extraction_generators:
            for seq in extraction_generator:
                print '\n'.join(seq)


if __name__ == "__main__":
    options = parse_args(argv)
    main(options)


