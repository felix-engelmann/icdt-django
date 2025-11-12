import pathlib
from collections import defaultdict

from tqdm import tqdm

from django.core.management.base import BaseCommand
from apps.faculty.models import Person
from apps.grants.models import Proposal, Sponsor, Investigator

import pandas as pd


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)
        # parser.add_argument("awardfile", type=pathlib.Path)

    def handle(self, *args, **options):
        # proposals = {}
        sponsor = defaultdict(set)

        excel = pd.ExcelFile(options["file"])

        for sheet_name in excel.sheet_names:
            # print(sheet_name)
            if "FY" in sheet_name and "Prop" in sheet_name:
                df = pd.read_excel(excel, sheet_name=sheet_name, header=0)
                for _, row in tqdm(df.iterrows()):
                    # print(row)
                    clean = {}
                    clean["wd_id"] = row["WD Proposal ID"]
                    clean["ps_id"] = row["PS Proposal ID"]
                    clean["title"] = row["Proposal Title"]
                    clean["report_date"] = row["Report Date"]
                    clean["fiscal_year"] = row["Fiscal Year"]

                    clean["direct_cost"] = row["Proposal Sponsor Direct Cost"]
                    clean["fa_cost"] = row["Proposal Sponsor F&A Cost"]

                    revst = {k: v for v, k in Proposal.STATUS.items()}
                    clean["status"] = revst[row["Proposal Status"]]

                    clean = {
                        k: None if c == "" or c != c else c for k, c in clean.items()
                    }

                    pi = Person.objects.get_or_create(employee_id=row["PI Empl ID"])[0]

                    sponsor = Sponsor.objects.get_or_create(spn_id=row["Sponsor ID"])[0]
                    sponsor.name = row["Sponsor Name"]
                    sponsor.federal = "Non" not in row["Federal/Non-Federal"]
                    sponsor.type = row["Sponsor Type"]
                    sponsor.level = row["Sponsor Level"]
                    sponsor.save()

                    clean["sponsor"] = sponsor

                    prime_id = row["Prime Sponsor ID"]
                    if prime_id == prime_id:
                        sponsor = Sponsor.objects.get_or_create(spn_id=prime_id)[0]
                        sponsor.name = row["Prime Sponsor Name"]
                        sponsor.federal = "Non" not in row["Prime Federal/Non-Federal"]
                        sponsor.type = row["Prime Sponsor Type"]
                        sponsor.level = row["Prime Sponsor Level"]
                        sponsor.save()
                        clean["prime_sponsor"] = sponsor

                    # print(clean)

                    prop = Proposal.objects.get_or_create(**clean)[0]
                    Investigator.objects.get_or_create(
                        proposal=prop, person=pi, type=Investigator.PI
                    )

                    if row["Co PI Empl ID"] == row["Co PI Empl ID"]:
                        for coid in row["Co PI Empl ID"].split(","):
                            copi = Person.objects.get_or_create(
                                employee_id=coid.strip()
                            )[0]
                            Investigator.objects.get_or_create(
                                proposal=prop, person=copi, type=Investigator.CO_PI
                            )

                    # break
                # df.columns
