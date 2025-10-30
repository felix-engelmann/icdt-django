import csv
import json
import pathlib

from django.core.management.base import BaseCommand
from apps.courses.models import Course, Semester, CourseOffering
from apps.faculty.models import Person


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        data = []
        with open("data/2024-Salaries-Combined.csv") as f:
            c = csv.DictReader(f)
            for line in c:
                data.append(line)

        manual_names = json.load(open("data/manual_names.json"))

        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                # print(row)
                course = Course.objects.get(
                    program=row["COURSE_CODE"].split(" ")[0],
                    level=int(row["COURSE_CODE"].split(" ")[1]),
                )
                # print(course)

                parts = row["OFFERED_PERIOD"].split(" ")
                rev = {k: v for v, k in Semester.SEMESTERS.items()}
                # print(rev[parts[0]], int(parts[1]))
                sem = Semester.objects.get_or_create(
                    year=int(parts[1]), term=rev[parts[0]]
                )[0]

                handlers = row["HANDLED_BY"].split(",")
                profs = []
                # TODO: make sure that the prof names are consistent with faculty
                for prof in handlers:
                    # print(prof.strip())
                    prof = prof.strip()

                    first_name = None
                    last_name = None

                    if prof in manual_names:
                        first_name = manual_names[prof][0]
                        last_name = manual_names[prof][1]

                    elif "." in prof:
                        parts = prof.split(".")
                        possibles = []
                        for poss in data:
                            if (
                                parts[1] == poss["Preferred Last Name"]
                                and parts[0] == poss["Preferred First Name"][0]
                            ):
                                possibles.append(poss)

                        if len(set([x["Identifier"] for x in possibles])) == 1:
                            first_name = possibles[0]["Preferred First Name"]
                            last_name = possibles[0]["Preferred Last Name"]
                            # print("found:",first_name, last_name)
                    else:
                        parts = prof.split(" ")
                        partset = set(parts)
                        poss = []
                        for paid in data:
                            if {
                                paid["Preferred First Name"],
                                paid["Preferred Last Name"],
                            } == partset:
                                poss.append(paid)
                        if len(set([x["Identifier"] for x in poss])) == 1:
                            first_name = poss[0]["Preferred First Name"]
                            last_name = poss[0]["Preferred Last Name"]
                        elif len(parts) == 2:
                            first_name = parts[0]
                            last_name = parts[1]
                            # print("found:",first_name, last_name)

                    if prof == "No.Available":
                        continue

                    if not (last_name and first_name):
                        print("missing", row)
                        raise Exception()

                    p = Person.objects.get_or_create(
                        first_name=first_name, last_name=last_name
                    )[0]
                    profs.append(p)

                offering = CourseOffering.objects.get_or_create(
                    course=course,
                    period=sem,
                    limit=row["ACTUAL_LIMIT"],
                    enrolled=row["TOTAL_ENROLLED"],
                )[0]
                offering.lecturers.set(profs)
