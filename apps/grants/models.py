from django.db import models

from apps.faculty.models import Person


# Create your models here.


class Investigator(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE)
    PI = "PI"
    CO_PI = "CO-PI"
    TYPE = {
        PI: "PI",
        CO_PI: "CO PI",
    }
    type = models.CharField(max_length=10, choices=TYPE)


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    spn_id = models.CharField(max_length=20, unique=True)
    federal = models.BooleanField(default=False)

    level = models.CharField(max_length=10)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Proposal(models.Model):
    wd_id = models.CharField(max_length=50, null=True)
    ps_id = models.CharField(max_length=50, null=True)

    NOT_FUNDED = "not_funded"
    AWARD_RECEIVED = "received"
    PENDING = "pending"
    NO_DATA = "no_data"
    STATUS = {
        NOT_FUNDED: "Not Funded",
        AWARD_RECEIVED: "Award Received",
        PENDING: "Submitted to Sponsor/Pending",
        NO_DATA: "No Award Data",
    }

    status = models.CharField(max_length=20, choices=STATUS)

    title = models.CharField(max_length=200)

    investigators = models.ManyToManyField(through=Investigator, to=Person)

    report_date = models.DateField(null=True)

    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True)
    prime_sponsor = models.ForeignKey(
        Sponsor, on_delete=models.SET_NULL, null=True, related_name="prime_proposals"
    )

    direct_cost = models.DecimalField(decimal_places=2, max_digits=10)
    fa_cost = models.DecimalField(decimal_places=2, max_digits=10)

    fiscal_year = models.IntegerField()
