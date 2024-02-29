# Generated by Django 5.0.1 on 2024-02-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipc', '0004_patent_client_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedpdffile',
            name='client_company_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='uploadedpdffile',
            name='client_contact_info',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='uploadedpdffile',
            name='country_filing_destination',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='uploadedpdffile',
            name='country_origin',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]