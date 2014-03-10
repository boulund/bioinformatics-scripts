#!/usr/bin/env python
# Count all unique reads mapped to something in the
# output from vmatch, due to the implementation it
# is rather slow, but worry not -- it does work!

from sys import argv
import re


files =[]
for i in xrange(len(argv)-1):
    files.append(open(argv[i+1],'r'))

# Regex to match the sample name from the first line of each file
regex_sample = re.compile(r'gutmeta/([A-Z0-9-_\.]*.raw.\d).fq')
# Match the gene/read description into group 1
regex_gene = re.compile(r'^.{3}\d\d.{3}([A-Z0-9a-z_:]{10,45})')
regex_read = re.compile(r'([\w\_:/#]+)\s+\d\s+[-\d]+\s{3,4}\d+\.\d\de-')
print "Filename         SampleName             Mappings  Ugenes  Ureads"
for file in files:
    # Counter for counting number of mappings
    counter = 0
    # Set for keeping unique read/gene names
    unique_reads = set()
    unique_genes = set()
    line = file.readline()
    sample_name = re.search(regex_sample,line)
    if sample_name is not None:
            #print sample_name.group(1) 
            sample_name = sample_name.group(1)
    for line in file:
        hit = re.search(regex_gene,line)
        if hit is not None:
            #print hit.group(1)
            unique_genes.add(hit.group(1))
            counter = counter + 1
        hit = re.search(regex_read,line)
        if hit is not None:
            #print hit.group(1)
            unique_reads.add(hit.group(1))
    print "%-15s  %-22s %8i  %6i   %5i" % (file.name, sample_name, counter, len(unique_genes), len(unique_reads))
