
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), label = 'Upload Oligo File(s):')
    #Uses 'multiple' attribute to create a MultiValueDict

from .models import user_input

class RefForm(forms.ModelForm):
    class Meta:
	model = user_input
	fields = ('reference',)
        labels = {'reference': ('Enter Reference Sequence:')}	
