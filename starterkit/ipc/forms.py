# forms.py

from django import forms
from .models import UploadedFile,Patent,UploadedPdfFile
from django_countries.fields import CountryField


class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PdfFileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedPdfFile
        fields = ['file','client_company_name','client_contact_info','country_origin','country_filing_destination']


class PatentForm(forms.ModelForm):
    patent_date = forms.DateField(input_formats=['%Y-%m-%d', '%d/%m/%y'],required=False)
    country = CountryField()

    class Meta:
        model = Patent
        fields = ['patent_title', 'patent_owner', 'patent_description', 'patent_date','client_company_name','client_contact_info','country_origin','country_filing_destination']