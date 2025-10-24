from django.contrib import admin
from .models import Semester, Course, CoursOffering
# Register your models here.

admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(CoursOffering)
