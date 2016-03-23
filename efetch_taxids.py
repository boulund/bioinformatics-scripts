#!/usr/bin/env python3.5
# Fredrik Boulund 2015
# Fetch taxids from GenBank via ACCNO
# Input is list of ACCNO 

from sys import argv, exit
from requests import get

if len(argv) < 2:
    print("usage: efetch_taxids.py FILE")
    print("Fredrik Boulund 2015")
    print("Fetch TAXIDs from Genbank using ACCNOs.")
    print("Enter filename of file with one ACCNO per line.")
    exit()

with open(argv[1]) as f:
    for line in f:
        accno = line.strip()
        payload = {"db": "nuccore", 
                   "id": accno,
                   "rettype": "fasta",
                   "retmode": "xml"}
        xml = get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=payload)
        try:
            taxid = xml.text.split("taxid>")[1].split("<")[0]
        except IndexError:
            print("{}\t{}".format(accno, ""))
        print("{}\t{}".format(accno, taxid))
