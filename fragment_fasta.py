#!/usr/bin/env python
# Fredrik Boulund 2015
# Fragment sequences from a FASTA file 

from read_fasta import read_fasta
from sys import argv, exit, maxint
import argparse
from random import randint, choice


def parse_args(argv):
    """Parse commandline arguments.
    """

    desc = """Sample sequences from FASTA files with replacement. Fredrik Boulund 2015"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("FASTA", 
            help="FASTA file to sample from.")
    parser.add_argument("-n", metavar="N", dest="n", required=True, type=int,
            help="Number of sequences to create from FASTA file [%(default)s].")
    parser.add_argument("-s", "--strip", dest="strip", action="store_true",
            default=False,
            help="Strip fasta headers to minimum size to reduce output filesize [%(default)s].")
    parser.add_argument("-l", "--length", dest="length", metavar="L", type=int,
            default=76,
            help="""Length of sequences to create from FASTA file [%(default)s],
                    cant be bigger than {} or any sequence in the file.""".format(maxint))

    if len(argv)<2:
        parser.print_help()
        exit()
    
    options = parser.parse_args()
    return options


def fragment_fasta(fastafile, options):
    """Sample sequences from FASTA.
    """

    seqs = [(header, seq) for header, seq in read_fasta(fastafile, keep_formatting=False)]

    for n in xrange(0, options.n):
        header, seq = choice(seqs)
        seqlen = len(seq)
        if seqlen < options.length:
            print "ERROR: Cannot sample fragment of length {} from sequence {} with length {}".format(options.length, header, seqlen)
        if options.strip:
            print ">{}".format(n)
        else:
            print ">{}_{} {} length={}".format(header.split()[0], n, " ".join(header.split()[1:]), options.length)
        startpos = randint(0, seqlen-options.length)
        print seq[startpos:startpos+options.length]


if __name__ == "__main__":
    options = parse_args(argv)
    fragment_fasta(options.FASTA, options)
