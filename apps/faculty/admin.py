from django.contrib import admin
from .models import Person, Department

# Register your models here.
admin.site.register(Person)
admin.site.register(Department)