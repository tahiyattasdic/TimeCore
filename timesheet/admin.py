# timesheet/admin.py
from django.contrib import admin
from .models import TimePunch

# Register your models here.
admin.site.register(TimePunch)