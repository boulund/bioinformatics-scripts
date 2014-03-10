#!/usr/bin/env python
# Parses the outputted files from Vmatch
# and stores information in a big matrix
# for usage in ShotgunFunctionalizeR.


from sys import argv, exit
import re

if len(argv)<2:
    print "Usage: script.py vmatchoutputfile(s)...\n"\
          "If more than one output in one file, it will be treated as coming"\
          "from the same 'master file'"
    exit()

# Regexes for extracting the interesting information
regex_inputfile = re.compile(r'/([^/]*).fq.*\.gz ')
regex_argeneid = re.compile(r'(ARGENE......)')
regex_readid = re.compile(r'\s(\S+:\S+:\S+)\s')

# Read the (true) number of counts of all reads in each input file. 
# This information is read from a file on disk, 
# containing zgrep-output as such:
# file1:142352
# file2:235725
# ....
regex_filenamereads = re.compile(r'^(.+)\.fq.*\.gz:(\d+)')
total_reads_file = open('/home/boulund/gutmeta/number_of_sequences.txt')
arg000lookup = {} # Init
for line in total_reads_file:
    hit = re.match(regex_filenamereads,line)
    if hit is not None:
        arg000lookup[hit.group(1)] = hit.group(2)



# Go through ALL files and extract information about
# input filenames, ARGENE000000-descriptors and counts.
# Store this information in 'listing'-hash indexed by 
# input filenames
listing = {} # Init
for filename in argv[1:]:
    file = open(filename)
    # The following couple of lines assume that only one
    # input file produced this outputfile being read.
    # If an input file was split and run in two instances of 
    # Vmatch but outputted to the same file, this will 
    # make sure that hits from both parts will be counted
    # to the same original input file.
    line = file.readline()
    if line.startswith("#"): # It is is a specificatione line from vmatch
        hit_inputfile = re.search(regex_inputfile,line)
        if hit_inputfile is not None:
            cur_inputfile = hit_inputfile.group(1)
            listing[cur_inputfile] = {} # Init the key for this file

    # Match the argeneID and if current read has not yet been 
    # matched against anything, increment the argeneID-counter
    # by one
    identified_reads = set() #empty set for storing read IDs
    for line in file:
        argenehit = re.search(regex_argeneid,line)
        readhit = re.search(regex_readid,line)
        if readhit is not None:
            if readhit.group(1) in identified_reads:
                #print "ALREADY FOUND", readhit.group(1)
                pass
            else:
                identified_reads.add(readhit.group(1))
                if argenehit is not None:
                    argeneid = argenehit.group(1) # The ID identified on this line
                    try: # if this fails, it is the first occurrence of this argene ID
                        listing[cur_inputfile][argeneid] = listing[cur_inputfile][argeneid]+1
                    except KeyError: 
                        listing[cur_inputfile][argeneid] = 1 # set the identified number to 1
        else:
            #print "PANIC!!!! Found no read ID - is it not Illumina data?"
            pass

# Create a set of all unique argene IDs found in any file
unique_ids_set = set() # Init
for inputfile in listing:
    for argeneid in listing[inputfile]:
        unique_ids_set.add(argeneid)




###############################################################################
##                          PRINTOUT                                         ##
###############################################################################

# Sort the list of input filenames for sorted printing to ShotgunFunctionalizeR table...
sorted_listing = listing.keys()
sorted_listing.sort()
# Printout of a table formatted to suit ShotgunFunctionalizeR, i.e.: (tabseparated)
# GeneFamily FILE1   FILE2   FILE3   FILE4   ...
# ARG001    1   3   4   2
# ARG002    0   3   0   1
# ...
# 
# Print the first two rows, containing inputfilenames and the number of
# unmapped reads (ARGENE000000) for each file, respectively.
firstline = "GeneFamily"
secondline = "ARGENE000000".strip()
output_listing = [] # Will contain input filename columns to output
for inputfilename in sorted_listing:
    if ".raw.1" in inputfilename:
        try:
            No_reads_mapped = []
            # Count the number of reads not mapped to anything (total - reads mapped)
            [No_reads_mapped.append(int(values)) for argeneids,values in listing[inputfilename].iteritems()]
            No_reads_not_mapped = int(arg000lookup[inputfilename]) - sum(No_reads_mapped)
            
            # Only add current input file to output if there was 
            # more than 1 read mapped
            if sum(No_reads_mapped) > 1:
                firstline = firstline+"\t"+inputfilename.strip()
                secondline = secondline+"\t"+str(No_reads_not_mapped / \
                             float(arg000lookup[inputfilename])).strip()
                # Add this input filename to the columns to be printed
                output_listing.append(inputfilename) 
        except KeyError:
            print "\t?",
            quitstring = "Catastrophic error: It seems '"+inputfilename+\
                         "' has no match in number_of_sequences.txt"        
            exit(quitstring)
print firstline
print secondline
# Print the remaining rows, one row for each unique argeneid
# For each argeneID, print the number of reads mapped from each inputfile
for argeneid in unique_ids_set:
    linestring = argeneid.strip()
    for inputfile in output_listing:
        if argeneid in listing[inputfile]: 
            linestring = linestring+"\t"+str(listing[inputfile][argeneid] / \
                         float(arg000lookup[inputfilename]) ).strip()
        else:
            linestring = linestring+"\t0"
    print linestring
