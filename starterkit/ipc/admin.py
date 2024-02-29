from django.contrib import admin
from .models import UploadedFile,IpcModelSymbol,Patent

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(IpcModelSymbol)
admin.site.register(Patent)