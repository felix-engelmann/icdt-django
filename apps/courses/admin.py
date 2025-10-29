from django.contrib import admin
from .models import Semester, Course, CoursOffering
# Register your models here.

admin.site.register(Semester)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code',"type","title","undergrad","graduate")
    list_filter = ("type","undergrad","graduate")

admin.site.register(Course, CourseAdmin)

class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course',"period","get_lecturers")
    list_filter = ("course","period","lecturers")

    def get_lecturers(self, obj):
        return ",".join([str(p) for p in obj.lecturers.all()])

admin.site.register(CoursOffering, CourseOfferingAdmin)
