#!/usr/bin/python
# Small script that will assess the time required
#to run vmatch with different settings.

import os
from sys import argv
import re

print argv

timeo = "/usr/bin/time -p -ao tid."
vmatch = [" vmatch -s -showdesc 45 -l 25 -dnavsprot 11 -q "]
#vmatch = [" vmatch -showdesc 45 -s -complete -h 2 -dnavsprot 11 -q ",\
#          " vmatch -showdesc 45 -s -complete -h 5p -dnavsprot 11 -q ",\
#          " vmatch -showdesc 45 -s -complete -dnavsprot 11 -q ",\
#          " vmatch -showdesc 45 -s -l 25 -h 2 -dnavsprot 11 -q "]
ending = " /home/boulund/softwareevaluation/ardb >> vmatchoutput."

# ... command line for each input file
for i in xrange(1,len(argv)):
    callstring = timeo+str(i)+vmatch[0]+argv[i]+ending+str(i)
    print callstring
    # Run Vmatch once...
    for b in xrange(1): os.system(callstring)
