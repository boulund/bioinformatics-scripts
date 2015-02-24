#!/usr/bin/env python
# Script cuts qnr genes into a multitude of pieces and runs
# hmmsearch on the result to evaluate the sensitivity and specificity
# of the model and hmmsearch.
# Fredrik Boulund 20110203

from sys import argv, exit
from os import path, system
from random import randint, random, choice, sample
from FB_functions import read_fasta
from optparse import OptionParser
from fluff import parse_hmmsearch_output, classify_qnr
from math import sqrt
import re


desc="""Script cuts qnr genes into a multitude of pieces and runs
 hmmsearch on the result to evaluate the sensitivity and specificity
 of the model and hmmsearch.
\nFredrik Boulund 20110209"""

usage = "script.py qnrseq.pfa [options]"

parser = OptionParser(usage=usage,description=desc)

parser.add_option("-p", "--probability", dest="probability", type="float", 
                  default=0, help="set probability of amino acid mutation, 0<=p<1 [default=%default]")
parser.add_option("-r", "--replicates", dest="replicates",
                  help="number of replicates [default=%default]",type="int", default=1000)
parser.add_option("-l", "--fraglength", dest="fraglength", type="int",
                  help="maximum fragment length, will be reduced to longest sequence in source file if too long [default=%default]", default=210)
parser.add_option("-R", dest="R", action="store_true",
                  help="Create and run R-scripts to plot data [default=%default]", default=False)
parser.add_option("-M", "--useModel", dest="model",
                  help="Use the given HMMer Model", default=False)

(options, args) = parser.parse_args()

if len(argv)<2:
    print parser.print_help()
    exit()



# Read QNR-sequences from fasta and store sequences in list of tuples
seqlist = read_fasta(args[0])

##---------------------------------------------------------------------------##
##                       DATA FOR FRAGMENT CREATION                          ##
##---------------------------------------------------------------------------##

# The number of different fragment lengths to be created:
MAXIMUM_FRAGMENT_LENGTH = options.fraglength  # max value is ~210 (213) for Qnr

# Number of fragments per fragment length:
NUMBER_OF_FRAGMENTS_PER_LENGTH = options.replicates

# Set of Qnr classes:
#qnr_set = set(['QnrA','QnrB','QnrC','QnrD','QnrS'])
qnr_set=set([])

# Determine the minimum sequence length
# (sets upper limit for fragment starting point)
# ALSO, create two sets of sequences; one with QNR-sequences and one without
SEQUENCE_MINLENGTH = 5000 # sufficiently large number
qnrseqlist = []
nonqnrseqlist = []
qnr_re = re.compile(r'Qnr\w')
for seqid,sequence in seqlist:
    if len(sequence) < SEQUENCE_MINLENGTH:
        SEQUENCE_MINLENGTH = len(sequence) 
    if "Qnr" in seqid:
        # The following regex will insert all
        # types of Qnr-genes seen in the source file
        # into the set of valid Qnr classes
        hit = re.search(qnr_re, seqid)
        if hit is not None:
            qnr_set.add(hit.group())
        # Append the current sequence to the qnrseqlist
        qnrseqlist.append((seqid,sequence))
    else:
        nonqnrseqlist.append((seqid,sequence))

# SEQUENCE_MINLENGTH is now not longer than minimum sequence length in src file
if MAXIMUM_FRAGMENT_LENGTH > SEQUENCE_MINLENGTH:
    MAXIMUM_FRAGMENT_LENGTH = SEQUENCE_MINLENGTH-1

# Read probability of per amino acid error from command line option:
if options.probability > 1.0:
    print "Probability was incorrectly entered, needs 0<p<1"
    exit()
else:
    P_MUTATION = options.probability

# Set of valid amino acid residues:
aa_list = set(['A','C','D','E','F','G','H','I','K','L','M',
               'N','P','Q','R','S','T','V','W','Y'])


# Create a list of fragment sizes, starting from 1 amino acid 
# up to MAXIMUM_FRAGMENT_LENGTH using stepsize 1 amino acid.
fragment_lengths = range(10, MAXIMUM_FRAGMENT_LENGTH, 1)


##---------------------------------------------------------------------------##
##                              FRAGMENT CREATION                            ##
##---------------------------------------------------------------------------##

outseq = "fragments.pfa"
outfile = open(outseq,"w")

# Loop over each fragment length
for fragment_length in fragment_lengths:
    
    # Loop over current fragment length 
    for fragment_number in xrange(1,NUMBER_OF_FRAGMENTS_PER_LENGTH+1):
        # Randomly select a source sequence for fragment creation by
        # first randomly chosing between Qnr and non-qnr.
        # Second, select one class of Qnr.
        # Third, randomly select one sequence to fragmentize.
        
        # Randomly select between Qnr and non-Qnr:
        qnr = random() > 0.5
        if qnr:
            # Randomly select a Qnr class
            random_qnr_class = ''.join(sample(qnr_set,1))
            # Randomly select one sequence from Qnr
            # until correct class found
            random_src_seq = randint(0,len(qnrseqlist)-1)
            while True:
                    if random_qnr_class in qnrseqlist[random_src_seq][0]:
                        break
                    else:
                        random_src_seq = randint(0,len(qnrseqlist)-1)
            
            # Unzip the current (randomly selected) sequence
            cur_seqid, cur_seq = qnrseqlist[random_src_seq]
            cur_seqlength = len(cur_seq)
            # Create random (valid) starting point within sequence length
            random_starting_point = randint(0, cur_seqlength - fragment_length) 
            # Compute the endpoint according to current fragment length
            endpoint = random_starting_point + fragment_length
            # Cut fragment from random_starting_point -> endpoint
            cur_fragment = cur_seq[random_starting_point:endpoint]
            
            # If mismatches are wanted; for each amino acid in fragment
            # throw random number and if less than P_MUTATION we 
            # randomly select one amino acid residue in its place
            # If P_MUTATION == 0 there can never be mutations
            if P_MUTATION > 0.0:
                cur_fragment_mut = ''
                for aa in cur_fragment:
                    utfall = random()
                    if utfall < P_MUTATION:
                        # Sample a random aa that is not the current
                        cur_fragment_mut = ''.join([cur_fragment_mut,
                                                ''.join((sample(aa_list-set(aa),1)))])
                    else:
                        # No mutation occurs
                        cur_fragment_mut = ''.join([cur_fragment_mut, aa])
                cur_fragment = cur_fragment_mut
        else: 
            # Randomly select one non-Qnr sequence
            random_src_seq = randint(0,len(nonqnrseqlist)-1)
            
            # Unzip the current (randomly selected) sequence
            cur_seqid, cur_seq = nonqnrseqlist[random_src_seq]
            cur_seqlength = len(cur_seq)
            # Create random (valid) starting point within sequence length
            random_starting_point = randint(0, cur_seqlength - fragment_length) 
            # Compute the endpoint according to current fragment length
            endpoint = random_starting_point + fragment_length
            # Cut fragment from random_starting_point -> endpoint
            cur_fragment = cur_seq[random_starting_point:endpoint]
            
            # If mismatches are wanted; for each amino acid in fragment
            # throw random number and if less than P_MUTATION we 
            # randomly select one amino acid residue in its place
            # If P_MUTATION == 0 there can never be mutations
            if P_MUTATION > 0.0:
                cur_fragment_mut = ''
                for aa in cur_fragment:
                    utfall = random()
                    if utfall < P_MUTATION:
                        # Sample a random aa that is not the current
                        cur_fragment_mut = ''.join([cur_fragment_mut,
                                                ''.join((sample(aa_list-set(aa),1)))])
                    else:
                        # No mutation occurs
                        cur_fragment_mut = ''.join([cur_fragment_mut, aa])

                cur_fragment = cur_fragment_mut
       
        # Write fragment to disk with new identifier: 
        # >fragment_length__random_starting_point__sequenceID
        outfile.write(''.join([">",str(fragment_length),"__",str(random_starting_point),"__",cur_seqid[1:],"\n",
                       cur_fragment,"\n"]))

# Close file for HMMer
outfile.close()




##---------------------------------------------------------------------------##
##                          RUN HMMSEARCH ON FRAGMENTS                       ##
##---------------------------------------------------------------------------##

# For each of the six models (-QnrA, -QnrB, -QnrC, -QnrD, -QnrS, all)
# run hmmsearch and store output in convenient file
#models = ["~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model11_pmqr-b_20110203/model11_pmqr-b.hmm"]
         #"~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model09_pmqr_20110203/model9.hmm"]#,
         #"~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model10_pmqr-a_20110203/model10_pmqr-a.hmm",
         #"~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model12_pmqr-c_20110203/model12_pmqr-c.hmm",
         #"~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model13_pmqr-d_20110203/model13_pmqr-d.hmm",
         #"~/qnr-search_project/hmmprofiles/profileconstruction/20110203-models_for_evaluation/model14_pmqr-s_20110203/model14_pmqr-s.hmm"]

if options.model:
    models = [str(options.model)]
else:
    models = ["~/qnr-search_project/hmmprofiles/profileconstruction/20110221-models_for_parameter_estimation/trainingmodel.hmm"]

modelnames = ["trainingmodel"]

#modelnames = ["PMQR"]#,"PMQR-QnrA","PMQR-QnrB","PMQR-QnrC","PMQR-QnrD","PMQR-QnrS"]


r_filenames = [] # Stores the filenames for use in R plotting later
for index in xrange(0,len(models)):
    modelpath = path.expanduser(models[index])
    hmmsearch_file = "hmmsearched_fragments.model"+modelnames[index]
    hmmsearchcall = "hmmsearch --notextw -o "+hmmsearch_file+" "+modelpath+" "+outseq
    #print hmmsearchcall
    system(hmmsearchcall)
   

    # Parse the hmmsearch output to retrieve sequence IDs and domain scores 
    # (Sequence IDs are then parsed to produce the tables with 
    # score, fragment_length, starting position information).
    score_id_tuples, dbpath = parse_hmmsearch_output(hmmsearch_file)

    
    #if options.R:
    # From the information retrieved, output to tab-separated file for use in R
    data_structure = {}
    for seq_score, dom_score, seqid in score_id_tuples: # Unzip score_id_tuples
        frag_length, starting_point, rest = seqid.split("__")
        
        # Insert the domain score and the starting point into the dictionary
        try:
            data_structure[frag_length].extend([dom_score]) #+"\t"+starting_point])
        except KeyError: # happens first time this frag_length is seen
            data_structure[frag_length] = [dom_score] #+"\t"+starting_point]
   
    
    # Print the domain score data to an R readable tab format
    stats_filename = "statistics_model"+modelnames[index]+".tab"
    stats_file = open(stats_filename,'w')
    r_filenames.append(stats_filename)
    sorted_fraglengths = data_structure.keys()
    sorted_fraglengths.sort()
    # Print a header line with as many columns as maximum number of fragment hits
    headerline = "Fraglength"
    for col in xrange(1,options.replicates+1):
        headerline = ''.join([headerline,"\t","r",str(col)])
    stats_file.write(headerline+"\n")
    for fraglength in sorted_fraglengths:
        line = fraglength
        for stat in data_structure[fraglength]:
            line = line+"\t"+stat
        stats_file.write(line+"\n")

    #else:
    print "k\tm\tc\tOBJF"
    k = 0.09
    for i in xrange(0,50):
        k = k + 0.01
        m = -1.0
        for ii in xrange(0,20):
            m = m + 1
            c = 49
            for iii in xrange(0,35):
                c = c + 1
                FN = 0.0
                FP = 0.0
                TP = 0.0
                TN = 0.0
                for seq_score, dom_score, seqid in score_id_tuples:
                    fraglength, startingpoint, header = seqid.split("__")
                    primary_classification = classify_qnr(fraglength, dom_score, 
                                                          func=lambda L: k*L+m, 
                                                          longseqcutoff=c)
                    
                    # Count false positives/negatives
                    if primary_classification and "Qnr" in header:
                        TP = TP + 1
                    elif primary_classification and not "Qnr" in header:
                        FP = FP + 1
                    elif not primary_classification and not "Qnr" in header:
                        TN = TN + 1
                    else:
                        FN = FN + 1
                

                TPR = TP/(TP+FN)
                FPR = FP/(FP+TN)
                if FPR == 0:
                    OBJF = sqrt(TPR)/(FPR+0.00001)
                else:
                    OBJF = sqrt(TPR)/FPR
                print k, m, c, OBJF 
                #print modelnames[index], "FN:", FN, "FP:", FP, "TPR:",TP/(TP+FP), "FPR:",FP/(FP+TN)




if options.R:
    # Constructs R scripts for each model and runs them in R BATCH mode,
    # they output plots to pdf-files. 
    for index in xrange(0,len(models)):
        r_script = open("r_script"+str(index),'w')
        r_script.write('d<-read.delim("'+r_filenames[index]+'")\n')
        r_script.write('d.ordered<-d[order(d$Fraglength),]\n')
        r_script.write('fl.max<-apply(d.ordered[,2:'+str(options.replicates+1)+'], 1, max, na.rm=T)\n')
        r_script.write('fl.min<-apply(d.ordered[,2:'+str(options.replicates+1)+'], 1, min, na.rm=T)\n')
        r_script.write('fl.median<-apply(d.ordered[,2:'+str(options.replicates+1)+'], 1, median, na.rm=T)\n')
        r_script.write('fl.99quant<-apply(d.ordered[,2:'+str(options.replicates+1)+'], 1, quantile, na.rm=T, prob=.99)\n')
        r_script.write('fl.01quant<-apply(d.ordered[,2:'+str(options.replicates+1)+'], 1, quantile, na.rm=T, prob=.01)\n')
        
        # Initiate PDF-file and set plot main title
        r_script.write('pdf(file="boxplot.'+modelnames[index]+'.pdf")\n')
        if options.probability > 0:
            main_title = (modelnames[index]+" vs "+path.basename(args[0]))
            sub_title = ("Maxlength="+str(MAXIMUM_FRAGMENT_LENGTH)+" "+
                         "#frgmts="+str(NUMBER_OF_FRAGMENTS_PER_LENGTH)+" P_mut="+str(P_MUTATION))
        else: 
            main_title = (modelnames[index]+" vs "+path.basename(args[0]))
            sub_title = ("Maxlength="+str(MAXIMUM_FRAGMENT_LENGTH)+" "+
                         "#frgmts="+str(NUMBER_OF_FRAGMENTS_PER_LENGTH))
        
        # Plot the data, omitting the first row since it contains the fragment lengths
        r_script.write('plot(d.ordered$Fraglength, fl.max, type="o", pch=25, cex=0.25, ylim=c(0, max(fl.max)+10), xlim=c(0, max(d$Fraglength)+10), main="'+main_title+'", sub="'+sub_title+'" ,ylab="Score", xlab="Fragment length" )\n')
        r_script.write('lines(d.ordered$Fraglength, fl.min, type="o", pch=24, cex=0.25)\n')
        r_script.write('lines(d.ordered$Fraglength, fl.median, lty=2, type="o", pch=20, cex=0.25)\n')
        r_script.write('lines(d.ordered$Fraglength, fl.99quant, lty=3, cex=0.25)\n')
        r_script.write('lines(d.ordered$Fraglength, fl.01quant, lty=3, cex=0.25)\n')
        r_script.write('dev.off()\n')
        r_script.close()
        
        r_call = "R-2.11.1 CMD BATCH "+"r_script"+str(index)
        print r_call
        system(r_call)




