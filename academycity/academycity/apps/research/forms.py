from django import forms

class InputFileForm(forms.Form):
    title = forms.CharField(label='Research name', max_length=100)
    file = forms.FileField(label='Select a file', help_text='max. 250 kbytes')
