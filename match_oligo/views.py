from django.shortcuts import render, redirect
import django_excel as excel
import xlrd

from .forms import UploadFileForm, RefForm

def import_excel_view(request):
    if request.method == "POST":
        form1 = UploadFileForm(request.POST, request.FILES)
	form2 = RefForm(request.POST)
        if form1.is_valid() or form2.is_valid():
	    reference = form2.save(commit=False)
	    reference.save()
            oligo_input = request.FILES['file']
	    book = xlrd.open_workbook(file_contents=oligo_input.read())
	    sheet = book.sheet_by_index(0)
	    nrows = sheet.nrows
	    test_cell = sheet.cell_value(rowx=1, colx=1)
	    #test_cell_string = string(test_cell)
	    oligo_row = 0
	    oligo_col = 2
	    name_col = 1
	     
	    return render(request, 'match_oligo/test_excel_var.html', {'var': [test_cell] })
	else:    
	    return render(request, 'match_oligo/test2.html' , {'form2': form2})
		
    else:
	form1 = UploadFileForm()
	form2 = RefForm()
    
    return render(request, 'match_oligo/excel_input.html', {'form1': form1, 'form2': form2})




