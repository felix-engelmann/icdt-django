from django.contrib import admin

from apps.grants.models import Sponsor, Grant

# Register your models here.

class SponsorAdmin(admin.ModelAdmin):
    list_display = ("spn_id",'name')

admin.site.register(Sponsor, SponsorAdmin)

class GrantAdmin(admin.ModelAdmin):
    list_display = ("type","tid",'status',"get_investigators","title","federal","report_date","sponsor","total")
    list_filter = ("type",'status',"investigators","federal","report_date","sponsor")

    def get_investigators(self, obj):
        return ",".join([str(p) for p in obj.investigators.all()])


admin.site.register(Grant, GrantAdmin)