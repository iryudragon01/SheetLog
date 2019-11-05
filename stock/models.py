from django.db import models
from django.urls import reverse
from datetime import datetime


# Create your models here.
class Item(models.Model):
    objects: models.manager
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    type = models.PositiveSmallIntegerField(choices=[(1, 'ticket'), (2, 'Air Pay'), (3, 'food')])

    def __unicode__(self):
        return self.name


class LogSheet(models.Model):  # log sheet
    objects: models.manager
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    version = models.PositiveIntegerField()  # index by version
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class TopUp(models.Model):  # fill up
    objects: models.manager
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    worker = models.CharField(max_length=200)
    version = models.PositiveIntegerField(default=0)
    date_log = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('stock:detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.item.name


class Income(models.Model):
    objects: models.manager
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    objects: models.manager
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class TempExpense(models.Model):
    objects: models.manager
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField()


# create model for template form
class DateTimeTemplate(models.Model):
    objects: models.manager
    date = models.DateField(default=datetime.now())
    time = models.TimeField(default=datetime.now())

    def get_absolute_url(self):
        return reverse('stock:getenddate',kwargs={'id': self.id})
