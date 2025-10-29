from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Person(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name