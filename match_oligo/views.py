from django.shortcuts import render, redirect
import django_excel as excel

from .forms import UploadFileForm

def import_excel_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
	    return render(request, 'match_oligo/test1.html', {'form': form})
	else:    
	    return render(request, 'match_oligo/test2.html' , {'form': form})
		
    else:
	form = UploadFileForm()

    return render(request, 'match_oligo/excel_input.html' , {'form': form})
