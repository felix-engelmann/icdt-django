import csv
import pathlib

from django.core.management.base import BaseCommand, CommandError
from apps.courses.models import Course


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                print(row)
                Course.objects.get_or_create(code=row['COURSE_CODE'], title=row["TITLE"], type=row["TYPE"],
                                             undergrad="UG" in row["GRAD_LEVEL"], graduate="Grad" in row["GRAD_LEVEL"])