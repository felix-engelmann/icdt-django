from django.urls import reverse
from django.utils.html import format_html, format_html_join


def link_listing(objs, revname, attr="title"):
    links = [
        format_html(
            '<a href="{}">{}</a>',
            reverse(revname, args=[p.id]),
            getattr(p, attr),
        )
        for p in objs
    ]
    return format_html_join("", "<li>{}</li>", ((link,) for link in links)) or "(None)"
