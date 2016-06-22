__author__ = 'kssindy'
import sys
#sys module allows you to access variables (such as files)_Use sys.argv[N]

from Bio.Seq import Seq
#imports Seq from Bio.Seq

reference_file = open(sys.argv[1], 'rU')
#reference_file is the file that you want to search the oligos against

merge_oligos = open(sys.argv[2], 'rU')
#merged oligo file

OutFileName2 = "oligo_match_results.txt"
OutFile2 = open(OutFileName2, 'w')
#These create and open files to which results can be written

reference_seq = reference_file.readline()
#Opens the reference file

CAPS_reference_seq = str.upper(reference_seq)
#converts reference file to upper case letters

for Line in merge_oligos:
#Searches merged 'globed' oligo file for following parameters

    StripLine = Line.strip('\n')
    #removes line ending characters

    StripSpace = StripLine.replace(" ", "")
    #removes anytime there is whitespace

    Column = StripSpace.split('\t')
    #seperates the line into a list of tab-delimited components

    search_seq = Column[2]
    #identifies column with oligo sequence (2 is actually 3 because numbering starts at 0)

    full_name = Column[1]
    #identifies column with oligo names (1 is actually 2 because numbering starts at 0)

    oligo_key = Column[0]
    #identifies column with oligo identifier eg KH23 (0 is actually 1 because  numbering starts at 0)

    matching_search = Seq(CAPS_reference_seq)
    #opens BioPython's Seq function on reference file and names it

    reverse_compliment = matching_search.reverse_complement()
    #creates a BioPython matching search for the reverse compliment of the reference file

    oligo_find = matching_search.find(search_seq)
    #Uses find function to search for oligos in reference file

    reverse_oligo_find = reverse_compliment.find(search_seq)
    #Uses find function to search for oligos in reverse compliment of reference file

    if oligo_find != -1 :
    #if the results is not -1 then move on with the script. -1 means failure or there was no match.

        if oligo_find != 0 :
        #if the result is not 0 then move on with the script

            OutputString = ("Here is the location oligo name and the location: %s, %s \n" % (oligo_key, oligo_find))
            #defines the oligos that pass the above tests or match to the reference file

            OutFile2.write(OutputString)
            #writes the matching oligos to the output file

    elif reverse_oligo_find != -1 :
    #if the REVERSE results is not -1 then move on with the script. -1 means failure or there was no match.

        if reverse_oligo_find !=0:
        #if the REVERSE results is not 0 then move on with the script

            OutputStringReverse = ("Here is the REVERSE location oligo name and the location: %s, %s \n" % (oligo_key, reverse_oligo_find))
            #defines the oligos that pass the above tests to the reverse reference file

            OutFile2.write(OutputStringReverse)
            #writes the matching oligos to the output file
