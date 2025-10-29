import csv
import pathlib
from collections import defaultdict

from django.core.management.base import BaseCommand
from apps.faculty.models import Department, Person
from apps.grants.models import Grant, Sponsor


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in fcsv:
                print(row)
                t = row["BEST_PROPOSAL_ID"][:3]
                tid = row["BEST_PROPOSAL_ID"][3:].replace("-","")

                revst = {k: v for v, k in Grant.STATUS.items()}
                status = revst[row["PROPOSAL_STATUS"]]

                fed = not ("Non-" in row['FED_STATUS'])

                spon = Sponsor.objects.get_or_create(name=row['SPONSOR_NAME'], spn_id=row['SPONSOR_ID'])[0]

                Grant.objects.get_or_create(type=t,tid=tid, status=status, federal=fed, sponsor=spon,
                                            report_date=row['REPORT_DATE'], total= row['PROPOSAL_SPONSOR_TOTAL'])