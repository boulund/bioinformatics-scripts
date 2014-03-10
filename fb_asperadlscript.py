#!/usr/bin/python
# Runs automated large downloads from SRA
# using the aspera connect program ascp.
# Input is a text file with sequence read IDs
# that are parsed to produce the remote
# location.
# Fredrik Boulund 2011-11-01

from os import system
from sys import argv, exit
import re

if len(argv) < 2:
    print """Usage: script.py txtfile \n
             # Runs automated large downloads from SRA
             # using the Aspera Connect software 'ascp'.
             # Input is a text file with sequence read IDs
             # that are parsed to produce the remote
             # location."""
    exit()

# Read all sequence IDs into a list
file = open(argv[1],'r')
downloads = []
for line in file:
    downloads.append(line.rstrip())
file.close()


## Set some basic settings ______________________
# path to ascp
ascppath = 'ascp ' #include trailing whitespace
# location of keyfile
keypath = '-i /local/aspera-2.4.7/connect/etc/asperaweb_id_dsa.putty ' #including trailing whitespace
# Resume of failed transfer, Throttle disks, disable encryption, recursive copy, limit speed to 90M, verbose
options = '-k1 -QTr -l90m -v '  #including trailing whitespace
# Username for ftp-access
user = 'anonftp@' 
# Download directory
downloadpath = ' .' 

# regular expression to match sra sequence read ids.
sraids = re.compile(r'(\w\w\w)(\d\d\d)(\d\d\d)') #e.g. srx000607 or SRA006744

## Commence the download of individual files ____
for seqid in downloads:
    if seqid is not '': # '' means EOF
        # Assume that input (in text file) are lines with SRA RUN IDs
        hit = re.match(sraids,seqid)
        if hit is not None:
            entire = hit.group(0)
            start = hit.group(1)
            middle = hit.group(2)
            print hit.group(0), hit.group(1), hit.group(2), hit.group(3)

            # Construct the FTP-path
            ftp_path = ''.join(["ftp-trace.ncbi.nih.gov:/sra/sra-instant/reads/ByRun/litesra/",\
                                start,"/",start+middle,"/",entire,"/",entire+".lite.sra"])
            print ftp_path
            
        
        # Compose the system call to ascp
        call = ascppath+keypath+options+user+ftp_path+downloadpath
        
        print call
        system(call)


#~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.putty -Q -l200m anonftp@ftp-private.ncbi.nlm.nih.gov:sra/static/SRX020/SRX020379 .
