#!/usr/bin/env python
from sys import argv, exit
from read_fasta import read_fastq

for count, record in enumerate(read_fastq(argv[1])):
    header, seq, header2, quals = record
    header = header.rsplit('.', maxsplit=1)[0] + '.' + str(count)
    print(header)
    print(seq)
    print(header2)
    print(quals)
