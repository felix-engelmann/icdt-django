from django.db import models

from apps.faculty.models import Person

# Create your models here.


class CourseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    program = models.CharField(max_length=40)
    level = models.IntegerField()
    type = models.ManyToManyField(CourseType)
    title = models.CharField(max_length=250, null=True)
    undergrad = models.BooleanField(null=True)
    graduate = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.program} {self.level}"

    class Meta:
        unique_together = ["program", "level"]
        ordering = ["program", "level"]


class Semester(models.Model):
    WINTER = "0WI"
    SPRING = "2SP"
    SUMMER = "4SU"
    AUTUMN = "8AU"
    SEMESTERS = {
        WINTER: "Winter",
        SPRING: "Spring",
        SUMMER: "Summer",
        AUTUMN: "Autumn",
    }
    year = models.IntegerField()
    term = models.CharField(max_length=5, choices=SEMESTERS)

    def __str__(self):
        return f"{self.term[1:]}{self.year % 100}"

    class Meta:
        ordering = ["year", "term"]


class Instructor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    offering = models.ForeignKey("CourseOffering", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.person)


class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.ForeignKey(Semester, on_delete=models.CASCADE)

    level_sub = models.IntegerField(null=True)
    level_suffix = models.CharField(max_length=5, null=True)

    limit = models.IntegerField()
    enrolled = models.IntegerField()

    lecturers = models.ManyToManyField(to=Person, through=Instructor)

    class Meta:
        ordering = ["course", "period"]

    def __str__(self):
        return f"{self.period} {self.course.program} {self.course.level}"
