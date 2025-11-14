from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.grants.models import Sponsor, Proposal, Investigator, Collaborator, Award

from apps.grants.utils import link_listing, rel_investigators


# Register your models here.


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("spn_id", "name", "federal", "level", "type")
    list_filter = ("federal", "level", "type")
    readonly_fields = ("proposals", "prime_proposals", "awards", "prime_awards")
    search_fields = ("name", "spn_id")

    def proposals(self, obj):
        return link_listing(obj.proposal_set.all(), "admin:grants_proposal_change")

    def prime_proposals(self, obj):
        return link_listing(obj.prime_proposals.all(), "admin:grants_proposal_change")

    def awards(self, obj):
        return link_listing(obj.award_set.all(), "admin:grants_award_change")

    def prime_awards(self, obj):
        return link_listing(obj.prime_awards.all(), "admin:grants_award_change")


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
    search_fields = ("wd_id", "ps_id", "title")

    inlines = [
        InvestigatorInline,
    ]

    def get_investigators(self, obj):
        return rel_investigators(obj.investigator_set.all())


admin.site.register(Proposal, ProposalAdmin)


class AwardAdmin(admin.ModelAdmin):
    list_display = (
        "wd_id",
        "proposal_link",
        "get_investigators",
        "title",
        "sponsor_link",
        "prime_sponsor_link",
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
    search_fields = (
        "wd_id",
        "ps_id",
        "title",
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

    def sponsor_link(self, obj):
        # reverse URL to change page for the author
        if obj.sponsor:
            url = reverse("admin:grants_sponsor_change", args=[obj.sponsor.id])
            return format_html('<a href="{}">{}</a>', url, obj.sponsor)

    def prime_sponsor_link(self, obj):
        # reverse URL to change page for the author
        if obj.prime_sponsor:
            url = reverse("admin:grants_sponsor_change", args=[obj.prime_sponsor.id])
            return format_html('<a href="{}">{}</a>', url, obj.prime_sponsor)

    def get_investigators(self, obj):
        return rel_investigators(obj.collaborator_set.all())


admin.site.register(Award, AwardAdmin)
