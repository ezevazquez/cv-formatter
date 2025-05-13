from django import forms

class CVUploadForm(forms.Form):
    file = forms.FileField(label="Subí tu CV (PDF)", required=True)
