from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from apps.grants.models import Sponsor, Proposal, Investigator


# Register your models here.


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("spn_id", "name", "federal", "level", "type")
    list_filter = ("federal", "level", "type")
    readonly_fields = ("proposals", "prime_proposals")
    search_fields = ("name", "spn_id")

    def proposals(self, obj):
        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:grants_proposal_change", args=[p.id]),
                p.title,
            )
            for p in obj.proposal_set.all()
        ]
        return (
            format_html_join("", "<li>{}</li>", ((link,) for link in links))
            or "(No proposals)"
        )

    def prime_proposals(self, obj):
        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse("admin:grants_proposal_change", args=[p.id]),
                p.title,
            )
            for p in obj.prime_proposals.all()
        ]
        return (
            format_html_join("", "<li>{}</li>", ((link,) for link in links))
            or "(No proposals)"
        )


admin.site.register(Sponsor, SponsorAdmin)


class InvestigatorInline(admin.TabularInline):
    model = Investigator


class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "wd_id",
        "status",
        "get_investigators",
        "title",
        "report_date",
        "sponsor",
        "prime_sponsor",
        "direct_cost",
        "fa_cost",
    )
    list_filter = (
        "status",
        "investigators",
        "report_date",
        "sponsor",
    )

    inlines = [
        InvestigatorInline,
    ]

    def get_investigators(self, obj):
        return ",".join([str(p) for p in obj.investigators.all()])


admin.site.register(Proposal, ProposalAdmin)
