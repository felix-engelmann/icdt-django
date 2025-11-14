from django.contrib import admin
from .models import Person, Department
from ..grants.utils import link_listing


# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "other_names",
        "employee_id",
        "department",
    )
    list_filter = ("department",)
    search_fields = (
        "first_name",
        "last_name",
        "other_names",
        "employee_id",
    )
    readonly_fields = ("proposals", "awards", "classes")

    def proposals(self, obj):
        return link_listing(
            obj.proposal_set.all(),
            "admin:grants_proposal_change",
        )

    def awards(self, obj):
        return link_listing(
            obj.award_set.all(),
            "admin:grants_award_change",
        )

    def classes(self, obj):
        return link_listing(
            obj.courseoffering_set.all(),
            "admin:courses_courseoffering_change",
            ("course", "period"),
        )


admin.site.register(Person, PersonAdmin)
admin.site.register(Department)
