from django.shortcuts import render, redirect
from django import forms

from .forms import XlsInputForm


# Create your views here.

def excel_input(request):
    if request.method == 'POST':
        form = XlsInputForm(request.POST, request.FILES)

        if form.is_valid():
            input_excel = request.FILES['input_excel']
            book = xlrd.open_workbook(file_contents=input_excel.read())

    # your work with workbook 'book'

    else:
        form = XlsInputForm

    return render (request, 'match_oligo/excel_input.html', {'form': form})

