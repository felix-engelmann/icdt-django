import csv
import pathlib

from django.core.management.base import BaseCommand
from apps.faculty.models import Department, Person


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                print(row)
                dep = Department.objects.get_or_create(name=row["DEPARTMENT"])[0]
                Person.objects.get_or_create(name=row["NAME"], department=dep)