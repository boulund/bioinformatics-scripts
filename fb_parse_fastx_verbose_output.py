#!/usr/bin/env python
# Parse the number of discarded reads from
# fastq_quality_trimmer verbose output.

from sys import argv, exit
import re

if len(argv)<2:
    print "Need filename argument"
    exit()


# Regular expression to match number of discarded reads and 
regex_nd = re.compile(r'discarded (\d+)')
regex_in = re.compile(r'Input: (\d+)')
regex_ut = re.compile(r'Output: (\d+)')

# A dictionary to hold each filename as key
filenames = {}
file = open(argv[1])
cur_filename = ''
for line in file:
    if ".gz" in line:
        cur_filename = line.strip()
        filenames[cur_filename] = []
    input = re.search(regex_in,line)
    if input is not None:
        filenames[cur_filename].append(input.group(1))
    output = re.search(regex_ut,line)
    if output is not None:
        filenames[cur_filename].append(output.group(1))
    nd = re.search(regex_nd,line)
    if nd is not None:
        filenames[cur_filename].append(nd.group(1))

# Sort the keys for ordered output
sorted_filenames = filenames.keys()
sorted_filenames.sort()

# Output to a long list for easy manual interpretation,
# refer to the line printed in next output group for
# output suitable to a ShotgunFunctionalizeR table
previous_individuals = set()
individual_sum = {}
individual_discarded_reads = {}
print "Filename\tInput\tOutput\tDiscarded"
for filename in sorted_filenames:
    print '\t'.join([filename,filenames[filename][0],filenames[filename][1],filenames[filename][2]])
    new_individual = filename.split("_")[0]
    if new_individual in previous_individuals:
        individual_sum[new_individual] = int(individual_sum[new_individual])+int(filenames[filename][1])
        individual_discarded_reads[new_individual] = int(individual_discarded_reads[new_individual])+int(filenames[filename][2])
    else:
        individual_sum[new_individual] = int(filenames[filename][1])
        individual_discarded_reads[new_individual] = int(filenames[filename][2])
        previous_individuals.add(new_individual)


# OUTPUT BELOW FOR SIMPLE ADDING TO TAB SEPARATED TABLE
# Sort the keys to output in correct order
sorted_names = individual_sum.keys()
sorted_names.sort()
longstring = ''
for name in sorted_names:    
    print name,individual_sum[name],individual_discarded_reads[name]
    longstring = longstring+("\t"+str(individual_sum[name]))
print longstring
