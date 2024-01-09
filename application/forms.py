# forms.py
from django import forms
from .models import Applicant, Documents

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'  # or specify the fields you want in the form

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'
