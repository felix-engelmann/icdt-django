from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from apps.grants.models import Sponsor, Proposal, Investigator, Collaborator, Award


# Register your models here.


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("spn_id", "name", "federal", "level", "type")
    list_filter = ("federal", "level", "type")
    readonly_fields = ("proposals", "prime_proposals", "awards", "prime_awards")
    search_fields = ("name", "spn_id")

    def listing(self, revname, objs):
        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse(revname, args=[p.id]),
                p.title,
            )
            for p in objs
        ]
        return (
            format_html_join("", "<li>{}</li>", ((link,) for link in links)) or "(None)"
        )

    def proposals(self, obj):
        return self.listing("admin:grants_proposal_change", obj.proposal_set.all())

    def prime_proposals(self, obj):
        return self.listing("admin:grants_proposal_change", obj.prime_proposals.all())

    def awards(self, obj):
        return self.listing("admin:grants_award_change", obj.award_set.all())

    def prime_awards(self, obj):
        return self.listing("admin:grants_award_change", obj.prime_awards.all())


admin.site.register(Sponsor, SponsorAdmin)


class InvestigatorInline(admin.TabularInline):
    model = Investigator


class CollaboratorInline(admin.TabularInline):
    model = Collaborator


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


class AwardAdmin(admin.ModelAdmin):
    list_display = (
        "wd_id",
        "proposal_link",
        "get_investigators",
        "title",
        "sponsor",
        "prime_sponsor",
        "start_date",
        "end_date",
        "beginning_fiscal_year",
        "type",
    )
    list_filter = (
        "start_date",
        "end_date",
        "beginning_fiscal_year",
        "type",
        "investigators",
        "sponsor",
    )

    inlines = [
        CollaboratorInline,
    ]

    def proposal_link(self, obj):
        # reverse URL to change page for the author
        if obj.proposal:
            url = reverse("admin:grants_proposal_change", args=[obj.proposal.id])
            return format_html('<a href="{}">{}</a>', url, obj.proposal)

    proposal_link.short_description = "Proposal"

    def get_investigators(self, obj):
        return ",".join([str(p) for p in obj.investigators.all()])


admin.site.register(Award, AwardAdmin)
