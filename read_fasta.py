#!/usr/bin/env python3.5
# Fredrik Boulund 2015
# Yield sequences from FASTA file

def read_fasta(filename, keep_formatting=True):
    """
    Read sequence entries from FASTA file.

    Yields (header, seq) tuples.

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
        seq = []
        header = ""
        while fasta:
            if line == "": #EOF
                yield header, sep.join(seq)
                break
            elif line.startswith(">") and not first:
                yield header, sep.join(seq)
                header = line.rstrip()[1:]
                seq = []
            elif line.startswith(">") and first:
                header = line.rstrip()[1:]
                first = False
            else:
                seq.append(line.rstrip())
            line = fasta.readline()


def read_fastq(filename, strip_second_header=True):
    """
    Read sequence entries from FASTQ file.

    Assumes 4 line FASTQ format.
    Yields (header, seq, second_header, scores) tuples.
    """

    with open(filename) as fastq:
        line = fastq.readline()
        if not line.startswith("@"):
            raise IOError("Not FASTQ format? First line didn't start with @")
        while fastq:
            if line.startswith("@"):
                header = line.rstrip()
                seq = fastq.readline().rstrip()
                second_header = fastq.readline()
                if strip_second_header:
                    second_header = "+"
                scores = fastq.readline().rstrip()
                yield header, seq, second_header, scores
            elif line == "": # EOF
                yield header, seq, second_header, scores
                break
            line = fastq.readline()
