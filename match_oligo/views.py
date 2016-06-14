from django.shortcuts import render, redirect
import django_excel as excel

from .forms import UploadFileForm, RefForm

def import_excel_view(request):
    if request.method == "POST":
        form1 = UploadFileForm(request.POST, request.FILES)
	form2 = RefForm(request.POST)
        if form1.is_valid() and form2.is_valid():
	    reference = form.save(commit=False)
	    reference.save()
            filehandle = request.FILES['file']
	    return render(request, 'match_oligo/test1.html', {'form2': form2})
	else:    
	    return render(request, 'match_oligo/test2.html' , {'form2': form2})
		
    else:
	form1 = UploadFileForm(prefix="form1")
	form2 = RefForm(prefix="form2")
    
    return render(request, 'match_oligo/excel_input.html', {'form1': form1, 'form2': form2})




