import pathlib
from datetime import datetime

from tqdm import tqdm

from django.core.management.base import BaseCommand
from apps.faculty.models import Person
from apps.grants.models import Proposal, Sponsor, Investigator, Award, Collaborator

import pandas as pd


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("file", type=pathlib.Path)
        # parser.add_argument("awardfile", type=pathlib.Path)

    def handle(self, *args, **options):
        # proposals = {}

        def insert_sponsor(
            row,
            spn_id="Sponsor ID",
            name="Sponsor Name",
            federal="Federal/Non-Federal",
            type="Sponsor Type",
            level="Sponsor Level",
        ):
            sponsor = Sponsor.objects.get_or_create(spn_id=row[spn_id])[0]
            sponsor.name = row[name]
            sponsor.federal = "Non" not in row[federal]
            sponsor.type = row[type]
            sponsor.level = row[level]
            sponsor.save()
            return sponsor

        excel = pd.ExcelFile(options["file"])

        for sheet_name in excel.sheet_names:
            # print(sheet_name)
            if "FY" in sheet_name and "Prop" in sheet_name:
                df = pd.read_excel(excel, sheet_name=sheet_name, header=0)
                for _, row in tqdm(df.iterrows(), total=len(df)):
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

                    clean["sponsor"] = insert_sponsor(row)

                    prime_id = row["Prime Sponsor ID"]
                    if prime_id == prime_id:
                        clean["prime_sponsor"] = insert_sponsor(
                            row,
                            spn_id="Prime Sponsor ID",
                            name="Prime Sponsor Name",
                            federal="Prime Federal/Non-Federal",
                            type="Prime Sponsor Type",
                            level="Prime Sponsor Level",
                        )

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
            if "FY" in sheet_name and "Award" in sheet_name:
                df = pd.read_excel(excel, sheet_name=sheet_name, header=0)
                difftitle = []
                for _, row in tqdm(df.iterrows(), total=len(df)):
                    # print(row)
                    none_row = {
                        k: None if c == "" or c != c else c for k, c in row.items()
                    }
                    prop_ids = {}
                    prop_ids["wd_id"] = none_row["WD Proposal ID"]
                    prop_ids["ps_id"] = none_row["PS Proposal ID"]
                    proposal = Proposal.objects.filter(**prop_ids)

                    clean = {}
                    if proposal.count() > 0:
                        clean["proposal"] = proposal.first()
                    clean["wd_id"] = row["WD Award ID"]
                    clean["ps_id"] = row["PS Award ID - Filled Down"]
                    clean["title"] = row["Award Title"]
                    clean["type"] = row["Award Type"]
                    clean["start_date"] = row["Start Date"]
                    if "/" in clean["start_date"]:
                        clean["start_date"] = datetime.strptime(
                            clean["start_date"], "%m/%d/%Y"
                        )
                    clean["end_date"] = row["End Date (Updated)"]
                    clean["beginning_fiscal_year"] = row["Beginning FY"]

                    clean = {
                        k: None if c == "" or c != c else c for k, c in clean.items()
                    }

                    clean["sponsor"] = insert_sponsor(
                        row, federal="Sponsor Federal/Non-Federal"
                    )

                    prime_id = row["Prime Sponsor ID"]
                    if prime_id == prime_id:
                        clean["prime_sponsor"] = insert_sponsor(
                            row,
                            spn_id="Prime Sponsor ID",
                            name="Prime Sponsor Name",
                            federal="Federal/Non-Federal Prime",
                            type="Prime Sponsor Type",
                            level="Prime Sponsor Level",
                        )

                    awd = Award.objects.get_or_create(**clean)[0]

                    if row["PI Empl ID"] == row["PI Empl ID"]:
                        pi = Person.objects.get_or_create(
                            employee_id=int(row["PI Empl ID"])
                        )[0]
                        Collaborator.objects.get_or_create(
                            award=awd, person=pi, type=Investigator.PI
                        )
                    if row["Co PI EmpID(s)"] == row["Co PI EmpID(s)"]:
                        for coid in row["Co PI EmpID(s)"].split(","):
                            copi = Person.objects.get_or_create(
                                employee_id=coid.strip()
                            )[0]
                            Collaborator.objects.get_or_create(
                                award=awd, person=copi, type=Investigator.CO_PI
                            )

                    # this was only to test how much the award data matches with the proposal data
                    if proposal.count() == 100:
                        # print(proposal)
                        # print(row)
                        proposal = proposal.first()

                        if proposal.title != row["Award Title"]:
                            difftitle.append((row["Award Title"], proposal.title))

                        if proposal.sponsor.spn_id != row["Sponsor ID"] and False:
                            if (
                                proposal.sponsor.federal
                                == "Non"
                                not in row["Sponsor Federal/Non-Federal"]
                                or proposal.sponsor.level == row["Sponsor Level"]
                                or proposal.sponsor.type == row["Sponsor Type"]
                            ):
                                print(row["Sponsor ID"])
                                print(row["Sponsor Name"])
                                print(proposal.title)
                                print(proposal.sponsor)
                                print(proposal.sponsor.spn_id)
                                print("")
                                # break
                            # break

                        cpis = set(
                            proposal.investigator_set.filter(
                                type=Investigator.CO_PI
                            ).values_list("person__employee_id", flat=True)
                        )
                        print(cpis)
                        if row["Co PI EmpID(s)"] == row["Co PI EmpID(s)"]:
                            coids = set(
                                map(
                                    lambda x: x.strip(),
                                    row["Co PI EmpID(s)"].split(","),
                                )
                            )
                            print(coids)
                            if cpis != coids:
                                print(row)
                                print(proposal.investigator_set.all())
                                break
                        # break
                        pi = (
                            proposal.investigator_set.filter(type=Investigator.PI)
                            .values_list("person__employee_id")
                            .first()[0]
                        )
                        if int(pi) != int(row["PI Empl ID"]):
                            print(row)
                            print(pi)
                            print(proposal.investigator_set.all())
                            break

                        #

                        # break
                    # break

                # for aw, pr in difftitle:
                #    print(aw)
                #    print(pr)
