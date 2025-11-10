from django.contrib import admin
from .models import Semester, Course, CourseOffering, CourseType

# Register your models here.
from django.utils.translation import gettext_lazy as _

admin.site.register(CourseType)
admin.site.register(Semester)


class LevelListFilter(admin.SimpleListFilter):
    title = _("Course Level")

    parameter_name = "level"

    def lookups(self, request, model_admin):
        return [(str(i * 1000), f"{i * 1000}s") for i in range(1, 6)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                level__gte=int(self.value()), level__lt=int(self.value()) + 1000
            )
        return queryset


class CourseAdmin(admin.ModelAdmin):
    list_display = ("program", "level", "get_types", "title", "undergrad", "graduate")
    list_filter = ("program", LevelListFilter, "type", "undergrad", "graduate")

    def get_types(self, obj):
        return ",".join([str(p) for p in obj.type.all()])


admin.site.register(Course, CourseAdmin)


class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "level_sub",
        "level_suffix",
        "period",
        "enrolled",
        "limit",
        "get_lecturers",
    )
    list_filter = (
        "course__program",
        "period",
    )
    search_fields = ("lecturers__other_names",)

    def get_lecturers(self, obj):
        return ",".join([str(p) for p in obj.lecturers.all()])


admin.site.register(CourseOffering, CourseOfferingAdmin)
