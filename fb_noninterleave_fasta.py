#!/usr/bin/env python
# Reformat fasta files.
# Fredrik Boulund 2011

from sys import argv, exit

##---------------------------------------------------------------------------##
##                    READ FASTA FILE INTO LIST OF TUPLES                    ##
##---------------------------------------------------------------------------##
def read_fasta(filename):
    """
    Takes a filename and reads FASTA sequence information.

    Stores information in a list with (sequenceID,sequence)-tuples.

    Input:
        filename    name or path of the FASTA file to be read.
   
    Output:
        seqlist     list of tuples with sequenceID and sequence
                    read from the input FASTA file.
                    Note that sequence_identifier does not end in 
                    a newline character! This needs to be added 
                    to print sequences in correct format.

    Errors:
        (none)

    Fredrik Boulund, 2011
    """

    fasta_file = open(filename) # Open file at filename
    line = fasta_file.readline() # Read first line
    first = True # Boolean determining if it is the first sequence in file
    sequence = "" # Stores sequence information
    seqlist = [] # List to store tuples of seqid,sequence information
    while fasta_file:
        if first and line.startswith(">"):
            # If first occurrence of ">", treat it a bit different
            sequence_identifier = line.rstrip()
            line = fasta_file.readline()
            first = False
        
        elif line.startswith(">") and not first:
            # Store complete (previous) sequence and id in tuple into list
            sequence = "".join(sequence.split('\n')) # Remove embedded newlines
            seqlist.append((sequence_identifier,sequence)) 
            
            sequence = ""  # Reset sequence string
            sequence_identifier = line.rstrip() # Set new seqid
            line = fasta_file.readline()
        
        elif line == "": #EOF
            # Store complete (last) sequence and id in tuple into list
            sequence = "".join(sequence.split('\n')) # Remove embedded newlines
            seqlist.append((sequence_identifier,sequence))
            break
        
        else: # This is sequence territory
            sequence = ''.join([sequence,line])
            line = fasta_file.readline()

    return seqlist
######################### END read_fasta


# No real need for a main function...
if len(argv) < 2:
    print "usage: fb_noninterleave_fasta.py file.fasta"
    print "Prints to stdout"

sequences = read_fasta(argv[1])
for seq in sequences:
   print seq[0], "\n", seq[1]
