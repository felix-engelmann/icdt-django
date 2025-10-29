import csv
import pathlib
from collections import defaultdict

from django.core.management.base import BaseCommand
from apps.faculty.models import Department, Person


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            opts = defaultdict(set)
            for row in fcsv:
                print(row)
                for k,v in row.items():
                    opts[k].add(v)

            for k,v in opts.items():
                if len(v) < 10:
                    print(k,v)