from django.shortcuts import render
import xlrd
from Bio.Seq import Seq

from .forms import UploadFileForm, RefForm

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
            #uses biopython bio.seq package to create a reverse compliment of the submitted reference data in case oligo is in reverse compliment orientation

            #SUBMITTED DATA: OLIGO FILE
            #oligo_input = request.FILES['file']
            
            oligo_input =  request.FILES.getlist('file')
            print oligo_input
            print type(oligo_input)         
	    name_match = ''
#            name_match_list = []

            #accesses user submitted data from uploaded file
#           book = xlrd.open_workbook(file_contents=oligo_input.read())
            #uses xlrd package to open and read submitted file as excel sheet
#           sheet = book.sheet_by_index(0)
            #identifies which sheet in the excel file to use
#           nrows = sheet.nrows
            #sets handle to number of rows in identified excel sheet
#           sheet_name = sheet.name
            #sets handle to sheet name in identified excel sheet
        
            for xlsfile in oligo_input:
                print 'enter for'
                #OLIGO MATCH SCRIPT: add +1 to oligo_row until reach nrows (the total number of rows in the sh
                oligo_row = 1
                oligo_col = 2
                name_col = 1
                #sets variables to identify row and column.
                print type(oligo_input)
                print xlsfile
                book = xlrd.open_workbook(file_contents=xlsfile.read())
                #Creates string from 'ExcelInMemoryUploadedFile' with read() function
                sheet = book.sheet_by_index(0)
                nrows = sheet.nrows
                print oligo_row                
                print nrows
                
                for oligo in range(sheet.nrows):
                    cell = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
                    print cell

                    if oligo_row < nrows:
                        print 'enter if'
                        print cell
                        #oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
                        #using above variables, sets handle to cell in sheet where match search will begin
                        oligo_caps = cell.upper()
                        #uses biopython to ensure oligo from cell is all caps
                        oligo_find = ref_seq.find(oligo_caps)       
                        oligo_rev_find = ref_rev_comp.find(oligo_caps)
                        #uses biopython to look for oligo in reference and reverse compliment of reference
                        if oligo_find == -1 and oligo_rev_find == -1:
                            print "enter if2"
                            oligo_row += 1
                            #if there is no match (-1), go to next row (add +1 to oligo_row)
                        elif oligo_find != -1 or oligo_rev_find != -1:
                            print 'enter elif'
                            oligo_row += 1
                            name_match = sheet.cell_value(rowx=oligo_row, colx=name_col)
                            print name_match
 #                           name_match_list.extend((name_match,))
                            #if there is a match (0), set handle to that cell name
                      
              
            
            return render(request, 'match_oligo/output.html', {'var': [name_match] })
            #ADD WHAT TO DO WHEN DO NOT FIND A MATCH
        else:    
            return render(request, 'match_oligo/test2.html' , {'form2': form2})
                
    #if there is no data to be submitted disply empty forms
    else:
        form1 = UploadFileForm()
        form2 = RefForm()
    
    return render(request, 'match_oligo/user_input.html', {'form1': form1, 'form2': form2})

