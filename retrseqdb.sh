#!/bin/sh
# Retrieve sequences from database using
# the previously created index file
#
# Input:
#   seqID to retrieve
#   database path
#   output filename
#
# Example call:
#  retrseqdb.sh ASDF1134134.3_1 ~/database.fasta retrieved_sequences.fasta
#
# Requires a previously made index of the 
# database! (stored at database.fasta.index)
#
# It takes as input the sequence identifier
# to find and uses fgrep to find it in the 
# index file, from which it extracts the 
# binary offsets to the positions of the
# sequence in the large database file.
# It then retrieves the sequence from the
# database using 'dd' that "copies" the 
# information to stdout which in turn gets
# redirected to file upon completion.
# This behaviour using fgrep will extract
# several sequences if several sequences
# matches the ID supplied. This kind of
# provides the ability to do "fuzzy" 
# retrieval...
#
# Note that if retrieved.sequence.fasta 
# previously exists it will be appended,
# and the file may be larger than indended!
#
# Author: Fredrik Boulund 2010-06-29
# Freely adapted from Asif Tamuri's script
# on www.homepages.ucl.ac.uk/~ucbtaut/
#
# Some parts of the script has been improved
# by not dumping to a temporary file on disk, 
# something I hope will improve performance
# a little bit.

fgrep "$1" "$2.index" | while read start end header
do
    len=`echo "$end-$start" | bc`
    dd if=$2 skip=$start bs=1 count=$len status=noxfer #of=tmp.out
#    cat tmp.out
done >> "$3" #fbtmp/retrieved_sequences.fasta

# Cleanup
#rm -f tmp.out
