from django.db import models
from django.urls import reverse


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    type = models.PositiveSmallIntegerField(choices=[(1, 'ticket'), (2, 'Air Pay'), (3, 'food')])

    def __unicode__(self):
        return self.name


class LogSheet(models.Model):  # log sheet
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    version = models.PositiveIntegerField()  # index by version
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class TopUp(models.Model):  # fill up
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
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField(auto_now=True)


class TempExpense(models.Model):
    name = models.CharField(max_length=200)
    value = models.PositiveIntegerField()
    date_log = models.DateTimeField()

