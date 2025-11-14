from django.urls import reverse
from django.utils.html import format_html, format_html_join


def link_listing(objs, revname, attr=("title",)):
    links = [
        format_html(
            '<a href="{}">{}</a>',
            reverse(revname, args=[p.id]),
            ", ".join([str(getattr(p, a)) for a in attr]),
        )
        for p in objs
    ]
    return format_html_join("", "<li>{}</li>", ((link,) for link in links)) or "(None)"


def rel_investigators(objs):
    links = [
        format_html(
            '<a href="{}">{}</a>',
            reverse("admin:faculty_person_change", args=[p.person.id]),
            p,
        )
        for p in objs
    ]
    return format_html_join("", "<li>{}</li>", ((link,) for link in links)) or "(None)"
