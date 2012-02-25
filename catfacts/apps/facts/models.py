from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class PhoneNumber(models.Model):
    phonenumber = models.CharField('Phone number', max_length=20, unique=True)

    def __unicode__(self):
        return self.phonenumber


class DailyNumber(models.Model):
    dailynumber = models.ForeignKey('PhoneNumber')

    def __unicode__(self):
        return self.dailynumber.phonenumber


class CatFact(models.Model):
    fact = models.CharField(unique=True, max_length=130)
    approved = models.BooleanField("approved submission", default=False)

    def __unicode__(self):
        return self.fact
