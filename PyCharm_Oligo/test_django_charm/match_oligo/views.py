from django.shortcuts import render
import xlrd
from Bio.Seq import Seq
import urllib.request
import re

from .forms import UploadFileForm, RefForm, ChrLocForm
#Acceses form and model form from forms.py



def import_excel_view(request):
    new_line_oligo = 0
    if request.method == "POST":
    #if there is data to be submitted continue with script
        form1 = UploadFileForm(request.POST, request.FILES)
        form2 = RefForm(request.POST)
        form3 = ChrLocForm(request.POST)
        #handle assigned to user submitted data for each form.
#        if form1.is_valid() and (form2.is_valid() or form3.is_valid()):
        #ensures data submitted is valid. Blank cells in excel sheet are not valid and will stop iteration of file.
        if form2.is_valid():
            #SUBMITTED DATA: REFERENCE TEXT
            reference = form2.cleaned_data['reference']
            #accesses validated form input
            #reference = request.POST['reference']
            #accesses unvalidated form input
            #accesses user submitted reference data as dictionary by keyname
            ref_to_seq = Seq(reference)
            ref_seq = ref_to_seq.upper()
            #uses biopython bio.seq package to create sequence from the submitted data: reference string
            ref_rev_comp = Seq.reverse_complement(ref_seq)
            #uses biopython bio.seq package to create a reverse compliment of the submitted reference data
            chr_input_seq = ''
            chr_input_rev_seq = ''

        elif form3.is_valid():
            #SUBMITTED DATA: CHROMSOME REFERENCE LINK
            chrom = request.POST['chr']
            loc_start = request.POST['loc_start']
            loc_stop = request.POST['loc_stop']
            url = "http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=chr{}:{},{}".format(chrom, loc_start, loc_stop)
            print (url)

            chr_url = urllib.request.urlopen(url)
            chr_url_read = chr_url.read()
            chr_url_decode = chr_url_read.decode('utf-8')
            chr_input = re.sub('<.+>', '', chr_url_decode)
            chr_input_strip = chr_input.replace('\n','')
            chr_input_caps = chr_input_strip.upper()
            chr_input_seq = Seq(chr_input_caps)
            chr_input_rev_seq = Seq.reverse_complement(chr_input_seq)

            ref_seq = ''
            ref_rev_comp = ''

        if form1.is_valid():
            #SUBMITTED DATA: OLIGO FILE
            oligo_input =  request.FILES.getlist('file')
            #Accesses 'file' from match_oligo/forms.py and uses .getlist to access all items in the MultiValueDict
            no_matches = 0
            #Add +1 if find a match. If no matches (0) print "There were no matches found"
            name_match_list = []
            sheet_info_list = []
            #creates empty  list where  matches from all files will be stored
            new_line = "--"


            for xlsfile in oligo_input:
            #iterates through user uploaded files
                if new_line_oligo > 0:
                    name_match_list.extend((new_line,))
                new_line_oligo = 0
                saw_file = 0
                oligo_row = 0
                oligo_col = 2
                name_col = 0
                #sets variables to identify row and column. This needs to be reset for each file that is why it is in this for loop.

                book = xlrd.open_workbook(file_contents=xlsfile.read())
                #Uses xlrd package to open and read submitted file as excel sheet.
                #Creates string from 'ExcelInMemoryUploadedFile' with read() function.

                sheet = book.sheet_by_index(0)
                #identifies which sheet in the excel file to use
                nrows = sheet.nrows
                #sets handle to number of rows in identified excel sheet

                file_name = "{}".format(xlsfile)
                sheet_name = "Sheet: {}".format(sheet.name)
                oligo_total = "Total number of oligos searched: {}".format(sheet.nrows)


                sheet_info_list.extend((file_name,))
                sheet_info_list.extend((sheet_name,))
                sheet_info_list.extend((oligo_total,))
                sheet_info_list.extend((new_line,))

                for oligo in range(sheet.nrows):
                #iterates through items in identified file/sheet
                    cell = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
                    #using above variables, sets handle to the cell in the current sheet/file where match search will begin


#OLIGO MATCH SCRIPT: add +1 to oligo_row until reach nrows ie the total number of rows in the sheet. If find a match in ref_seq write to match_list.

                    if oligo_row < nrows:
                        oligo_caps = cell.upper()
                        #uses biopython to ensure oligo from cell is all caps
                        oligo_find = ref_seq.find(oligo_caps)
                        oligo_rev_find = ref_rev_comp.find(oligo_caps)
                        oligo_find_url = chr_input_seq.find(oligo_caps)
                        oligo_rev_find_url = chr_input_rev_seq.find(oligo_caps)
                        #uses biopython to look for oligo in reference and reverse compliment of reference
                        if oligo_find and oligo_find_url == -1 and oligo_rev_find and oligo_rev_find == -1 or cell == '':
                            oligo_row += 1
                            #if there is no match (-1), go to next row (add +1 to oligo_row)
                        elif oligo_find or oligo_find_url != -1 or oligo_rev_find or oligo_rev_find_url != -1:
                        #if there is a match (not -1, any other number is the index of the match), set handle to that cell name
                            name = sheet.cell_value(rowx=oligo_row, colx=name_col)
                            #assign handle to cell with match
                            name_match = str(name)
                            print (name_match)
                            #create string from cell name


                            #append any matches to name_match_list list
                            if saw_file < 1:
                                xls_match_file_name = "%s:" % xlsfile
                                name_match_list.extend((xls_match_file_name,))
                                name_match_list.extend((name_match,))
                            else:
                                name_match_list.extend((name_match,))
                            saw_file += 1
                            no_matches += 1
                            oligo_row += 1
                            new_line_oligo += 1



            return render(request, 'match_oligo/output.html', {'var': name_match_list, 'search_param': sheet_info_list,})
            #ADD WHAT TO DO WHEN DO NOT FIND A MATCH

    else:
        form1 = UploadFileForm()
        form2 = RefForm()
        form3 = ChrLocForm()
    return render(request, 'match_oligo/user_input.html', {'form1': form1, 'form2': form2, 'form3':form3})
    #if there is no data to be submitted disply empty forms
