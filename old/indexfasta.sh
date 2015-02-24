#!/bin/sh
# Creates a binary index file for large
# fasta files to quickly access sequences.
# It takes a regularily formatted fasta
# file as input and indexes it, outputting
# the index to 'filename.index'.
#
# Author: Fredrik Boulund 2010-06-29
# Pretty much copied verbatim from
# the script on Asif Tamuri's homepage,
# www.homepages.ucl.ac.uk/~ucbtaut/
# without any major modifications. 
# All credits goes to him for creating
# this script.

# Get byte offsets of sequence headers
fgrep -b ">" $1 > tmp.$1.headers.with.offset

# Extract just byte offsets
cut -f1 -d ":" tmp.$1.headers.with.offset > tmp.$1.offset.start

# Figure out the ending offsets of each sequence in two steps:
# 1) Copy the ending offsets but skip first line
sed "1d" tmp.$1.offset.start > tmp.$1.offset.end

# 2) Add the offset for the last sequence (i.e. EOF)
wc -c $1 | cut -f1 -d " " >> tmp.$1.offset.end

# Extract just the header lines for the index file
cut -f2 -d ":" tmp.$1.headers.with.offset | cut -f1 -d " " > tmp.$1.headers

# Merge all information in one index file
paste tmp.$1.offset.start \
      tmp.$1.offset.end \
      tmp.$1.headers > "$1.index"

# Cleanup
rm -f tmp.$1.headers.with.offset \
      tmp.$1.offset.start \
      tmp.$1.offset.end \
      tmp.$1.headers
