#!/bin/sh
# Download NCBI refseq bacterial genomes as FASTA
# Authors:
#  Fanny Berglund 2016
#  Fredrik Boulund 2016
# 
# Instructions:
# Retrieves only complete genomes, for other assemblies such as drafts or
# chromosomes or a specific bacteria change the ASSEMBLY variable below. 
#
# Changelog:
# [2016-05-11] boulund
# - Cleaned up a bit. Separated AWK scripts to reduce long lines.

JOBS=15

#### AWK SCRIPTS:
create_dirpaths='$12=="Complete Genome" && $11=="latest" { print $20 }'
create_filepaths='
BEGIN {
	FS=OFS="/";
	filesuffix="genomic.gff.gz";
}
{
	ftpdir=$0;
	asm=$6;
	file=asm"_"filesuffix;
	print ftpdir,file;
}'


# Create download folder and enter it
date=`date +%Y%m%d`
read -p "About to download NCBI RefSeq annotations from sequences marked as 'Complete Genome' from ftp.ncbi.nih.gov to $date."$'\nCtrl-C to abort, Press a key to continue.'
mkdir -p $date
cd $date

# Construct FTP file paths for each genome sequence to download
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt
awk -F "\t" "$create_dirpaths" assembly_summary.txt > ftpdirpaths
awk "$create_filepaths" ftpdirpaths > ftpfilepaths

# If GNU parallel is installed, download in parallel!
if hash parallel 2>/dev/null; then
	parallel --jobs $JOBS wget {} < ftpfilepaths
	parallel --jobs $JOBS gunzip {} ::: *gff.gz
else
	while read line; do
		wget $line
	done < ftpfilepaths
	gunzip *gff.gz
fi

