from django.db import models

from apps.faculty.models import Person
# Create your models here.

class CourseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=40)
    type = models.ManyToManyField(CourseType)
    title = models.CharField(max_length=250)
    undergrad = models.BooleanField()
    graduate = models.BooleanField()

    def __str__(self):
        return f"{self.code}"

class Semester(models.Model):
    SPRING = "0SP"
    SUMMER = "1SU"
    AUTUMN = "2AU"
    SEMESTERS = {
        SPRING: "Spring",
        SUMMER: "Summer",
        AUTUMN: "Autumn",
    }
    year = models.IntegerField()
    term = models.CharField(max_length=5, choices=SEMESTERS)

    def __str__(self):
        return f"{self.term[1:]}{self.year%100}"

class CoursOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.ForeignKey(Semester, on_delete=models.CASCADE)

    limit = models.IntegerField()
    enrolled = models.IntegerField()

    lecturers = models.ManyToManyField(Person)

    def __str__(self):
        return f"{self.period} {self.course.code}"

