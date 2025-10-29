from django.contrib import admin
from .models import Person, Department

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name',"last_name", "employee_id","department")
    list_filter = ("department",)

admin.site.register(Person, PersonAdmin)
admin.site.register(Department)