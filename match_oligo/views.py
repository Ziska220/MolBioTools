from django.shortcuts import render, redirect
import django_excel as excel
import xlrd
from Bio.Seq import Seq

from .forms import UploadFileForm, RefForm

def import_excel_view(request):
    if request.method == "POST":
        form1 = UploadFileForm(request.POST, request.FILES)
	form2 = RefForm(request.POST)
        if form1.is_valid() and form2.is_valid():
	    reference = form2.save(commit=False)
	    reference.save()
	    ref = reference
	    #ref_read = open(reference.read())
	    ref_str = str(ref)
	    ref_seq = Seq(ref_str)
	    ref_rev_comp = Seq.reverse_complement(ref_seq)

            oligo_input = request.FILES['file']
	    book = xlrd.open_workbook(file_contents=oligo_input.read())
	    sheet = book.sheet_by_index(0)
	    nrows = sheet.nrows
	    test_cell = sheet.cell_value(rowx=1, colx=1)
	    sheet_name = sheet.name
	    sheet_nrows = sheet.nrows	    
	 
	    oligo_row = 0
	    oligo_col = 2
	    name_col = 1

	    while oligo_row < nrows:
		oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
		oligo_caps = oligo.upper()
		oligo_find = ref_seq.find(oligo_caps)	
		oligo_rev_find = ref_rev_comp.find(oligo_caps)
		if oligo_find == -1 and oligo_rev_find == -1:
		    oligo_row += 1
		elif oligo_find ==0 or oligo_rev_find == 0:
		    name = sheet.cell_value(rowx=oligo_row, colx=name_col)
		    match = oligo_caps
		    break
	    
	    return render(request, 'match_oligo/test_excel_var.html', {'var': [test_cell, sheet_name, match, ref_seq] })
	else:    
	    return render(request, 'match_oligo/test2.html' , {'form2': form2})
		
    else:
	form1 = UploadFileForm()
	form2 = RefForm()
    
    return render(request, 'match_oligo/excel_input.html', {'form1': form1, 'form2': form2})




