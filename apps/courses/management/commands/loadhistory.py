import csv
import pathlib
from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from apps.courses.models import Course, Semester, CourseOffering
from apps.faculty.models import Person


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                print(row)
                course = Course.objects.get(code=row["COURSE_CODE"])
                print(course)

                parts = row["OFFERED_PERIOD"].split(" ")
                rev = {k:v for v,k in Semester.SEMESTERS.items()}
                print(rev[parts[0]], int(parts[1]))
                sem = Semester.objects.get_or_create(year=int(parts[1]), term=rev[parts[0]])[0]

                handlers = row["HANDLED_BY"].split(",")
                profs = []
                # TODO: make sure that the prof names are consistent with faculty
                for prof in handlers:
                    p = Person.objects.get_or_create(name=prof.strip())[0]
                    profs.append(p)

                offering = CourseOffering.objects.get_or_create(course=course, period=sem, limit=row['ACTUAL_LIMIT'], enrolled=row["TOTAL_ENROLLED"])[0]
                offering.lecturers.set(profs)