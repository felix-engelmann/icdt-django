from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=200)
    college = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Person(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    employee_id = models.IntegerField(null=True, unique=True)

    other_names = models.JSONField(null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
