from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Patients)
admin.site.register(Phlebotomist)
admin.site.register(Reporttracking)
admin.site.register(Testrecord)