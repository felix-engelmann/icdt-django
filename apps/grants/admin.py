from django.contrib import admin

from apps.grants.models import Sponsor, Grant

# Register your models here.

class SponsorAdmin(admin.ModelAdmin):
    list_display = ("spn_id",'name')

admin.site.register(Sponsor, SponsorAdmin)

class GrantAdmin(admin.ModelAdmin):
    list_display = ("type","tid",'status',"title","federal","report_date","sponsor","total")
    list_filter = ("type",'status',"federal","report_date","sponsor")

admin.site.register(Grant, GrantAdmin)