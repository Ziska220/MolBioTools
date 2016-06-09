from django.shortcuts import render, redirect
from django import forms

from .forms import NameForm


def name_input(request):

    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():

            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            name = form.save(commit=False)
            name.save()
            return redirect('/query/thanks/')
    else:
        form = NameForm()

    return render(request, 'query/home.html', {'form': form})

def thanks(request):
    return render (request, 'query/name.html')
