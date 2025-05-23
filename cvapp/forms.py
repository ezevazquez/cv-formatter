from django import forms
from .models import Employee

class CVUploadForm(forms.Form):
    file = forms.FileField(label="Subí tu CV (PDF)", required=True)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['uploaded_cv']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email']