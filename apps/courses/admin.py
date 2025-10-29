from django.contrib import admin
from .models import Semester, Course, CoursOffering, CourseType
# Register your models here.

admin.site.register(CourseType)
admin.site.register(Semester)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code',"get_types","title","undergrad","graduate")
    list_filter = ("type","undergrad","graduate")

    def get_types(self, obj):
        return ",".join([str(p) for p in obj.type.all()])


admin.site.register(Course, CourseAdmin)

class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course',"period","get_lecturers")
    list_filter = ("course","period","lecturers")

    def get_lecturers(self, obj):
        return ",".join([str(p) for p in obj.lecturers.all()])

admin.site.register(CoursOffering, CourseOfferingAdmin)
