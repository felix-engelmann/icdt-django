import os.path
import pathlib
from collections import defaultdict
from glob import glob
from typing import Literal, Counter

from django.core.management.base import BaseCommand
from apps.courses.models import Course, Semester, CourseOffering, Instructor
from pydantic import BaseModel, field_validator

from apps.faculty.models import Person


class Teaching(BaseModel):
    program: str
    number: int
    sub_number: int | None = None
    number_suffix: Literal["H", "E", "S", "L"] | None = None
    class_no: int
    class_type: str

    enrolled: int
    limit: int
    wait: int | None

    empl_id: list[tuple[str, str | None]]
    partial_semester: str | None = None

    @field_validator("class_type")
    def must_be_singleupper(cls, v: str):
        if v != v.upper() or v != v.strip() and len(v) != 1:
            raise ValueError("code must be single uppercase")
        return v

    @field_validator("program")
    def must_be_upper(cls, v: str):
        if v != v.upper() or v != v.strip():
            raise ValueError("code must be all uppercase")
        return v

    @field_validator("empl_id")
    def must_be_ids(cls, vs: list[tuple[str, None | str]]):
        for v in vs:
            if v[0] != v[0].strip() or not v[0].isnumeric():
                raise ValueError("not an employee id")
            if v[1]:
                if v[1] != v[1].strip() or v[1] != v[1].upper() or len(v[1]) != 2:
                    raise ValueError("not an employee type")
        return vs


class NameTeaching(Teaching):
    @field_validator("empl_id")
    def must_be_ids(cls, vs: list[tuple[str, None | str]]):
        for v in vs:
            if v[0] != v[0].strip():
                raise ValueError("not an employee id")
            if v[1]:
                if v[1] != v[1].strip() or v[1] != v[1].upper() or len(v[1]) != 2:
                    raise ValueError("not an employee type")
        return vs


def parse_emplidstr(employeepart: str) -> list[tuple[str, str | None]]:
    emplids = employeepart.split(", ")
    if len(emplids) == 1 and emplids[0] == "":
        emplids = []
    emplid_tuples = []
    for emplid in emplids:
        if "(" in emplid:
            emplid_parts = emplid.split("(")
            assert len(emplid_parts) == 2
            emplid_tuples.append((emplid_parts[0].strip(), emplid_parts[1][:-1]))
        else:
            emplid_tuples.append((emplid.strip(), None))
    return emplid_tuples


def parse_file(fn, cls):
    ret = {}
    with open(fn) as f:
        line = f.readline()
        parts = line.split(" ")
        # print(parts)
        f.readline()
        header = f.readline()
        with_wait = "+wait" in header
        last_t = None
        for line in f:
            if line.strip() == "":
                continue
            if line.startswith("INDependent study classes"):
                break
            # print(line)

            layout = "     CSE 1110             4791 L                                      ONLINE      14/0        11111111"
            layout = "     CSE 5194.01         37467 L                  T R     0935A-1055  BE0180      10/15       111111111"
            layout = "                                            and   T       0220P-0340  BE0120                  11111111"
            layout = "     CSE 1222       LMA   5186 L                  T R     0935A-1055  GA0451      19/24       11111111"
            layout = "     CSE 6469             5246 L                  T R     1110A-1230               0/20       11111111 (GR)"
            layout = "     CSx 1222  x      x   514x x           x    x     x   1130A    x  GW HOUSE 1 155/160     x111111111"
            layout = "     CSE  100             5412 L                                                  86/150      11111111"
            layout = "     CSx 1222  x      x   514x x           x    x     x   1130A    x  EA0163    x155/160     x111111111"
            if not with_wait:
                layout = "     CSE  100             5412 L                                                  86/150   M.Compton"
                layout = "     CSx 1222  x      x   514x x           x    x     x   1130A    x  EA0163    x155/160  x111111111"

            positions = [-1] + [i for i, c in enumerate(layout) if c == "x"]
            parts = []
            for start, end in zip(positions, positions[1:]):
                # print(start+1, end+1)
                parts.append(line[start + 1 : end + 1])
            parts.append(line[positions[-1] :])

            stripped = [p.strip() for p in parts]
            # print(stripped)

            if stripped[6] == "and":
                emplid_tuples = parse_emplidstr(stripped[-1])
                if len(emplid_tuples) > 0 and last_t:
                    last_t.empl_id += emplid_tuples
                continue

            enrollstr = stripped[10]
            wait = None
            if "+" in enrollstr:
                wait = int(enrollstr.split("+")[1])
                enrollstr = enrollstr.split("+")[0].strip()

            enr = int(enrollstr.split("/")[0])
            lim = int(enrollstr.split("/")[1])

            employeepart = stripped[-1]
            partial = None
            if employeepart.startswith("{"):
                curlypart = employeepart.split("}")
                assert len(curlypart) == 2
                partial = curlypart[0][1:]
                employeepart = curlypart[1]

            emplid_tuples = parse_emplidstr(employeepart)

            number_suffix = None
            sub_number = None
            number = stripped[1]
            if number[-1].isalpha():
                number_suffix = stripped[1][-1]
                number = number[:-1]

            if "." in number:
                number, sub_number = map(int, number.split("."))
            else:
                number = int(number)

            t = cls(
                program=stripped[0],
                number=number,
                sub_number=sub_number,
                number_suffix=number_suffix,
                class_no=stripped[3],
                class_type=stripped[4],
                enrolled=enr,
                limit=lim,
                wait=wait,
                empl_id=emplid_tuples,
                partial_semester=partial,
            )
            # print(t)
            if t.class_no not in ret:
                ret[t.class_no] = t
            last_t = t
    return ret


class Command(BaseCommand):
    help = "Closes the courses"

    def add_arguments(self, parser):
        parser.add_argument("path", type=pathlib.Path)

    def handle(self, *args, **options):
        name_id_map = defaultdict(list)
        if "schedule" in str(options["path"]):
            print("use the employee_id files")
            return
        for file in glob(str(options["path"]) + "/**/*.txt", recursive=True):
            print(file)

            splitted = file.split("/")
            print(splitted)
            pos = splitted.index("barrett.3")
            if pos >= 0:
                splitted[pos + 1] = "schedule"

            name_file = "/".join(splitted)

            nums = parse_file(file, Teaching)

            if os.path.exists(name_file):
                names = parse_file(name_file, NameTeaching)
                # print(nums)
                # print(names)

                t: Teaching
                t: NameTeaching
                for t in nums.values():
                    if t.class_no not in names:
                        print("missing class", t.class_no, file)
                        break
                    nt = names[t.class_no]
                    # print(t)
                    # print(nt)
                    tm = t.model_dump_json(
                        include={
                            "program",
                            "number",
                            "sub_number",
                            "number_suffix",
                            "class_no",
                            "class_type",
                            "limit",
                        }
                    )
                    ntm = nt.model_dump_json(
                        include={
                            "program",
                            "number",
                            "sub_number",
                            "number_suffix",
                            "class_no",
                            "class_type",
                            "limit",
                        }
                    )
                    if tm != ntm:
                        print("#", t)
                        print("N", nt)
                        continue
                    if len(t.empl_id) == len(nt.empl_id):
                        # print("equate",t.empl_id, nt.empl_id )
                        for eid, name in zip(t.empl_id, nt.empl_id):
                            name_id_map[eid[0]].append(name[0])
                        # print("different length", t,nt)
                        # break

                # break

            # break
            # with open(options["file"]) as f:

        # print(name_id_map)
        for eid, n in name_id_map.items():
            print(eid, Counter(n))
            pass
        for eid, name_list in name_id_map.items():
            names = set(name_list)
            p = Person.objects.get_or_create(employee_id=eid)[0]
            if p.other_names:
                old = set(p.other_names)
            else:
                old = set()
            if len(names - old):
                p.other_names = list(old.union(names))
                p.save()

            if len(names):
                if not p.first_name:
                    p.first_name = ".".join(
                        map(lambda a: f"{a}.", list(names)[0].split(".")[:-1])
                    )
                if not p.last_name:
                    p.last_name = list(names)[0].split(".")[-1]
                p.save()
            # break
        # return

        for file in glob(str(options["path"]) + "/**/*.txt", recursive=True):
            print(file)
            nums = parse_file(file, Teaching)

            semester_number = int(file.split("/")[-1][:4])
            year = (semester_number - 1000) // 10
            term = semester_number % 10

            term_map = {
                0: Semester.WINTER,
                2: Semester.SPRING,
                4: Semester.SUMMER,
                8: Semester.AUTUMN,
            }
            print(year, term_map[term])

            semester = Semester.objects.get_or_create(
                year=2000 + year, term=term_map[term]
            )[0]

            for t in nums.values():
                # print(t)
                course = Course.objects.get_or_create(
                    program=t.program, level=t.number
                )[0]
                co = CourseOffering.objects.get_or_create(
                    course=course,
                    period=semester,
                    level_sub=t.sub_number,
                    level_suffix=t.sub_number,
                    limit=t.limit,
                    enrolled=t.enrolled,
                )[0]
                for lec in t.empl_id:
                    p = Person.objects.get_or_create(employee_id=lec[0])[0]
                    Instructor.objects.get_or_create(person=p, offering=co, type=lec[1])
                # break
            # break
