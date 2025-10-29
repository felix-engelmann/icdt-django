import csv
import pathlib

from django.core.management.base import BaseCommand, CommandError
from apps.courses.models import Course, CourseType


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                print(row)
                types = list(map(lambda x:x.strip(), row["TYPE"].split("/")))
                #print(types)
                type_objects = []
                for typ in types:
                    tobj = CourseType.objects.get_or_create(name=typ)[0]
                    type_objects.append(tobj)
                print(type_objects)
                program = row['COURSE_CODE'].split(" ")[0].upper()
                level = int(row['COURSE_CODE'].split(" ")[1])
                course = Course.objects.get_or_create(program=program, level=level, title=row["TITLE"],
                                             undergrad="UG" in row["GRAD_LEVEL"], graduate="Grad" in row["GRAD_LEVEL"])[0]
                course.type.set(type_objects)