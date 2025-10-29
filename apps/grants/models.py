from django.db import models

from apps.faculty.models import Person


# Create your models here.

class Investigator(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grant = models.ForeignKey("Grant", on_delete=models.CASCADE)
    PI = "PI"
    CO_PI = "CO-PI"
    TYPE = {
        PI: "PI",
        CO_PI: "CO PI",
    }
    type = models.CharField(max_length=10, choices=TYPE)

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    spn_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Grant(models.Model):
    AWP = "AWP"
    GRT = "GRT"
    TYPE = {
        AWP: "AWP",
        GRT: "GRT",
    }
    type = models.CharField(max_length=10, choices=TYPE)
    tid=models.CharField(max_length=50)

    NOT_FUNDED = "not_funded"
    AWARD_RECEIVED = "received"
    PENDING = "pending"
    NO_DATA = "no_data"
    STATUS = {NOT_FUNDED: 'Not Funded',
              AWARD_RECEIVED: 'Award Received',
              PENDING: 'Submitted to Sponsor/Pending',
              NO_DATA: 'No Award Data'}

    status = models.CharField(max_length=20)

    title= models.CharField(max_length=200)

    investigators = models.ManyToManyField(through=Investigator, to=Person)

    federal = models.BooleanField()

    report_date = models.DateField()

    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True)

    total = models.DecimalField(decimal_places=2, max_digits=10)



