
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

from .models import user_input

class RefForm(forms.Form):
    class Meta:
	model = user_input
	fields = ('reference',)
    	
