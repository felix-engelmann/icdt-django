import csv
import json
import pathlib
import sys
from collections import defaultdict
from tqdm import tqdm

from django.core.management.base import BaseCommand
from apps.faculty.models import Department, Person
from apps.grants.models import Grant, Sponsor, Investigator


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
            for row in tqdm(fcsv):
                # print(row)

                def create_person(name, dep=None, eid=None):
                    first_name = None
                    last_name = None
                    if name in manual_names:
                        first_name = manual_names[name][0]
                        last_name = manual_names[name][1]
                    else:
                        parts = set(name.split(" "))
                        poss = []
                        for paid in data:
                            if {paid['Preferred First Name'], paid['Preferred Last Name']} == parts:
                                poss.append(paid)
                        if len(set([x['Identifier'] for x in poss])) == 1:
                            first_name = poss[0]['Preferred First Name']
                            last_name = poss[0]['Preferred Last Name']

                    if first_name and last_name:
                        depo = None
                        if dep:
                            depo = Department.objects.get_or_create(name=dep)[0]

                        if not Person.objects.filter(employee_id=eid).exists():
                            Person.objects.get_or_create(first_name=first_name,
                                                         last_name=last_name,
                                                         department=depo,
                                                         employee_id=eid)
                    else:
                        raise Exception("unknown %s", name)

                create_person(row['PI_NAME'],row['PI_DEPARTMENT'],row['PI_EMPL_ID'])

        with open(options["file"]) as f:
            fcsv = csv.DictReader(f)
            for row in tqdm(fcsv):
                # print(row)
                t = row["BEST_PROPOSAL_ID"][:3]
                tid = row["BEST_PROPOSAL_ID"][3:].replace("-","")

                revst = {k: v for v, k in Grant.STATUS.items()}
                status = revst[row["PROPOSAL_STATUS"]]

                fed = not ("Non-" in row['FED_STATUS'])

                spon = Sponsor.objects.get_or_create(name=row['SPONSOR_NAME'], spn_id=row['SPONSOR_ID'])[0]

                pi = Person.objects.get(employee_id=row['PI_EMPL_ID'])
                #for copiname in zip(row['CO_PI_NAME'].split(","), row['CO_PI_EMPL_ID'].split(" ")):
                #for copiname in row['CO_PI_NAME'].split(","):
                #    if copiname.strip() == "":
                #        continue
                #    print("create copi", copiname)
                #    if not Person.objects.filter(employee_id=copieid.strip()).exists():
                #        if copiname.strip():
                #    create_person(copiname.strip(), None,None)
                    #try:
                    #    copi = Person.objects.get(employee_id=copieid.strip())
                    #except:
                    #    print(row)
                    #    sys.exit(1)
                # break

                gr = Grant.objects.get_or_create(type=t,tid=tid, status=status, federal=fed, sponsor=spon,
                                            report_date=row['REPORT_DATE'], total= row['PROPOSAL_SPONSOR_TOTAL'],
                                            title=row['PROPOSAL_TITLE'])[0]
                Investigator.objects.get_or_create(grant=gr, person=pi, type=Investigator.PI)