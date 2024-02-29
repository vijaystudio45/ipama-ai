
# Create your models here.
from django.db import models
from datetime import date
# from dja
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')


class UploadedPdfFile(models.Model):
    file = models.FileField(upload_to='pdf_uploads/')
    client_company_name = models.CharField(max_length=120, null=True, blank=True)
    client_contact_info = models.CharField(max_length=120, null=True, blank=True)
    country_origin = models.CharField(max_length=120, null=True, blank=True)
    country_filing_destination = models.CharField(max_length=120, null=True, blank=True)


class IpcModelSymbol(models.Model):
    symbol = models.CharField(max_length=5000, null=True, blank=True)
    text_body = models.CharField(max_length=5000, null=True, blank=True)
    edition = models.CharField(max_length=5000, null=True, blank=True)
    ref = models.CharField(max_length=5000, null=True, blank=True)
    section =  models.CharField(max_length=5000, null=True, blank=True)   # A63B
    main_class =  models.CharField(max_length=5000, null=True, blank=True)  # 41
    subclass =  models.CharField(max_length=5000, null=True, blank=True)      # /
    main_group =  models.CharField(max_length=5000, null=True, blank=True)  # 12
    subgroup =  models.CharField(max_length=5000, null=True, blank=True)



class Patent(models.Model):
    patent_title = models.CharField(max_length=120)
    patent_owner = models.CharField(max_length=120)
    client_company_name = models.CharField(max_length=120, null=True, blank=True)
    client_contact_info = models.CharField(max_length=120, null=True, blank=True)
    country_origin = models.CharField(max_length=120, null=True, blank=True)
    country_filing_destination = models.CharField(max_length=120, null=True, blank=True)
    patent_description = models.CharField(max_length=2000)
    patent_date = models.DateField(null=True, blank=True,default=date.today)
    Scopes = models.CharField(max_length=120, null=True,blank=True)
    cip_Edition	= models.CharField(max_length=120, null=True,blank=True)
    cip_Section	=  models.CharField(max_length=120, null=True,blank=True)
    cip_class	 = models.CharField(max_length=120, null=True,blank=True)
    cip_ubclass	 = models.CharField(max_length=120, null=True,blank=True)
    cip_Group	=  models.CharField(max_length=120, null=True,blank=True)
    cip_Subgroup	=  models.CharField(max_length=120, null=True,blank=True)
    Description = models.CharField(max_length=120,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)  
    

    def __str__(self):
        return f'Patent: {self.patent_title}'



