# Generated by Django 5.0.1 on 2024-01-31 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipc', '0002_patent_description_patent_scopes_patent_cip_edition_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedPdfFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdf_uploads/')),
            ],
        ),
    ]
