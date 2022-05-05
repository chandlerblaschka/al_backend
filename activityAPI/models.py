from tkinter import CASCADE
from django.db import models

# Create your models here.

class Master(models.Model):

    industry = models.CharField(max_length=50)
    oppNumber = models.CharField(max_length=25, blank=True)
    name = models.CharField(max_length=100)
    prodCode = models.CharField(max_length=6)
    request = models.CharField(max_length=25)
    sales = models.CharField(max_length=25)
    projManager = models.CharField(max_length=25)
    engineer = models.CharField(max_length=25)
    reqDate = models.DateField( blank=True, null=True)
    dueDate = models.DateField(blank=True, null=True)
    compDate = models.DateField( blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True)
    reqDate.editable = True
    dueDate.editable = True
    compDate.editable = True

class Input(models.Model):
    entry_date = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Master, on_delete=models.CASCADE)


