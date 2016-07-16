from django.shortcuts import render
import xlrd
from Bio.Seq import Seq

from .forms import UploadFileForm, RefForm
#Acceses form and model form from forms.py

def import_excel_view(request):
    if request.method == "POST":
    #if there is data to be submitted continue with script      
        form1 = UploadFileForm(request.POST, request.FILES)
        form2 = RefForm(request.POST)
        #handle assigned to user submitted data for each form.
        if form1.is_valid() and form2.is_valid():
        #ensures data submitted is valid. Blank cells in excel sheet are not valid and will stop iteration of file.
                
            #SUBMITTED DATA: REFERENCE TEXT
            reference = request.POST['reference']
            #accesses user submitted reference data as dictionary by keyname
            ref_to_seq = Seq(reference)
            ref_seq = ref_to_seq.upper()
            #uses biopython bio.seq package to create sequence from the submitted data: reference string
            ref_rev_comp = Seq.reverse_complement(ref_seq)
            #uses biopython bio.seq package to create a reverse compliment of the submitted reference data

            #SUBMITTED DATA: OLIGO FILE
            oligo_input =  request.FILES.getlist('file')
            #Accesses 'file' from match_oligo/forms.py and uses .getlist to access all items in the MultiValueDict              
            no_matches = 0
            #Add +1 if find a match. If no matches (0) print "There were no matches found"
            name_match_list = []
            #creates empty  list where  matches from all files will be stored
            

            for xlsfile in oligo_input:
            #iterates through user uploaded files
    
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
                        #uses biopython to look for oligo in reference and reverse compliment of reference
                        if oligo_find == -1 and oligo_rev_find == -1 or cell == '':
                            oligo_row += 1
                            #if there is no match (-1), go to next row (add +1 to oligo_row)
                        elif oligo_find != -1 or oligo_rev_find != -1:
                        #if there is a match (not -1, any other number is the index of the match), set handle to that cell name
                            no_matches += 1
                            oligo_row += 1
                            name = sheet.cell_value(rowx=oligo_row, colx=name_col)
                            #assign handle to cell with match
                            name_match = str(name)
                            #create string from cell name
                            name_match_list.extend((name_match,))
                            #append any matches to name_match_list list
   
            
            return render(request, 'match_oligo/output.html', {'var': name_match_list })
            #ADD WHAT TO DO WHEN DO NOT FIND A MATCH
                
    else:
        form1 = UploadFileForm()
        form2 = RefForm()
    return render(request, 'match_oligo/user_input.html', {'form1': form1, 'form2': form2})
    #if there is no data to be submitted disply empty forms
