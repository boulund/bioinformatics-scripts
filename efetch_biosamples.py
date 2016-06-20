#!/usr/bin/env python3.5
# Fredrik Boulund (c) 2016
# Efetch BioSample data from GenBank 

from sys import argv, exit
from collections import OrderedDict
from requests import get
import argparse


def parse_args():
    """
    Parse command line arguments.
    """
    desc = "Efetch BioSample information from NCBI. Fredrik Boulund (c) 2016."

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("BIOSAMPLES", 
            help="Text file with one BioSample accession per line.")
    parser.add_argument("-a", "--attribute", nargs="+", dest="attributes",
            help="""Attributes to include in output (can be specified 
            multiple times). Enclose attributes in quotation marks!""")
    parser.add_argument("-o", "--output", dest="output",
            default="biosamples_data.txt",
            help="Output filename (tab separated text) [default=%(default)s].")
    parser.add_argument("-d", "--dump-file", metavar="FILENAME", dest="dumpfile",
            default=False,
            help="Dump all the retrieved data to a text file.")

    if len(argv) < 2:
        parser.print_help()
        exit()

    return parser.parse_args()


def parse_biosamples(filename):
    """
    Parse biosample annos from file.
    """

    with open(filename) as f:
        for line in f:
            biosample = line.strip()
            yield biosample


def parse_attributes(text):
    """
    Return attribute:value pairs from NCBI E-fetch text response.
    """
    lines = text.split("\n")
    desc = lines[0].split(":")[1].strip()
    identifiers = lines[1][12:].split(";")
    organism = lines[2].split(":")[1].strip()
    attributes = {}
    accession = ""
    for line in lines[4:]:
        if line.strip().startswith("/"):
            try:
                attrib, value = line.strip("/ ").split("=", 1)
            except ValueError:
                print("ERROR parsing attribute:", line)
                exit(1)
            attributes[attrib] = value.replace('"', '')
        if line.startswith("Accession"):
            accession = line.split(":")[1].split("\t")[0].strip()
    attribs = [("Description", desc),
               ("Identifiers", identifiers),
               ("Organism", organism),
               ("Accession", accession),
               ("Attributes", attributes),
               ]
    return OrderedDict(attribs)


def efetch_biosample(accno, retry_attempts=2):
    """
    Use NCBI E-utils efetch to get info for biosample.
    Returns an empty string if no match is found for accno.
    """
    payload = {"db": "biosample", 
               "id": accno,
               "retmode": "text"}

    result = get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=payload)
    if result.ok:
        if result.text.startswith("Error"):
            print("WARNING: error occured for {}".format(accno))
            return 
        else:
            return result.text
    else:
        print("WARNING: no match for {}".format(accno))
        return 


def write_output(biosamples, outfilename, attribute_keys=None):
    """
    Writes BioSample attributes to tab separated text file.
    """

    if attribute_keys is None:
        keys = ["isolation source", 
                "host", 
                "host disease", 
                "geographic location", 
                "collection date"]
    else:
        keys = attribute_keys
    header = "Accession\tOrganism\tIdentifiers\tDescription"
    for key in keys:
        header = header+"\t"+key
    with open(outfilename, 'w') as outfile:
        outfile.write(header+"\n")
        for biosample in biosamples:
            outfile.write(biosample["Accession"]+"\t")
            outfile.write(biosample["Organism"]+"\t")
            outfile.write(" ".join(biosample["Identifiers"])+"\t")
            outfile.write(biosample["Description"]+"\t")
            for key in keys:
                try:
                    outfile.write(biosample["Attributes"][key]+"\t")
                except KeyError:
                    outfile.write("-\t")
            outfile.write("\n")

def write_dump(raw_data, dumpfile):
    """
    Write complete data dump.
    """
    with open(dumpfile, 'w') as outfile:
        for biosample in raw_data:
            outfile.write(biosample+"\n")


def main(biosamples_file, outputfile, attribute_keys, dumpfile=False):
    """
    Main function.
    """
    biosamples = []
    raw_data = []
    for biosample in parse_biosamples(biosamples_file):
        biosample_info = efetch_biosample(biosample)
        if biosample_info:
            biosamples.append(parse_attributes(biosample_info))
            raw_data.append(biosample_info)
    write_output(biosamples, outputfile, attribute_keys=attribute_keys)
    if dumpfile:
        write_dump(raw_data, dumpfile)


if __name__ == "__main__":
    options = parse_args()
    main(options.BIOSAMPLES, 
            options.output, 
            options.attributes, 
            options.dumpfile)
