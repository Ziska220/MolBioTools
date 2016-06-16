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
	    sheet_name = sheet.name
	    sheet_nrows = sheet.nrows	    
	 
	    oligo_row = 1
	    oligo_col = 2
	    name_col = 1

	    oligo_row_out = oligo_row
	    while oligo_row < nrows:
		oligo_row_start = oligo_row
		oligo = sheet.cell_value(rowx=oligo_row, colx=oligo_col)
		oligo_caps = oligo.upper()
		oligo_find = ref_seq.find(oligo_caps)	
		oligo_rev_find = ref_rev_comp.find(oligo_caps)
		if oligo_find == -1 and oligo_rev_find == -1:
		    oligo_now = oligo_caps
		    oligo_row_now = oligo_row
		    oligo_row += 1
		elif oligo_find ==0 or oligo_rev_find == 0:
		    print "pass elif"
		    print oligo_caps
		    oligo_now_elif = oligo_caps
		    name_test = sheet.cell_value(rowx=oligo_row, colx=name_col)
		    break
	    
	    return render(request, 'match_oligo/test_excel_var.html', {'var': [oligo_row_out, oligo_row_start, nrows, oligo_row_now, sheet_name, ref_seq, oligo_now, oligo_now_elif, name_test] })
	else:    
	    return render(request, 'match_oligo/test2.html' , {'form2': form2})
		
    else:
	form1 = UploadFileForm()
	form2 = RefForm()
    
    return render(request, 'match_oligo/excel_input.html', {'form1': form1, 'form2': form2})




