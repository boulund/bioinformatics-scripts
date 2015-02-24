#!/usr/bin/python
# Runs automated large downloads from SRA
# using the aspera connect program ascp.

from os import system
from sys import argv

if len(argv) < 2:
    print "Usage: script.py txtfile"


file = open(argv[1],'r')
downloads = []
for line in file:
    downloads.append(line.rstrip())
file.close()

# path to ascp
ascppath = '/home/boulund/.aspera/connect/bin/ascp '
# location of keyfile
keypath = '-i /home/boulund/.aspera/connect/etc/asperaweb_id_dsa.putty '
# Resume of failed transfer, Throttle disks disable encryption recursive copy, limit speed to 90M, verbose
options = '-k1 -QTr -l90m -v ' 
# Username for ftp-access
user = 'anonftp@' 
# Download directory
downloadpath = ' .' 

for download in downloads:
    if download is not '':
        try:
            # Divide the address into protocol, site, source_folder  
            download_details = download.split("//")
            site = download_details[1] # e.g. ftp-ncbi.nih.gov
            source_folder = download_details[2] # e.g. bla/bla/source_folder/file000
            #print site, source_folder
        except IndexError:
            pass
            # Assume the current line is a correct ftp-address
            #site = download[6:26]
            #source_folder = download[27:]
            #print site, source_folder

        # Compose the system call to ascp
        call = ascppath+keypath+options+user+site+":/"+source_folder+downloadpath
        print call
        system(call)


#~/.aspera/connect/bin/ascp -i ~/.aspera/connect/etc/asperaweb_id_dsa.putty -Q -l200m anonftp@ftp-private.ncbi.nlm.nih.gov:sra/static/SRX020/SRX020379 .

