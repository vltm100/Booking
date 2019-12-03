from django.db import models
# Create your models here.
from django import forms
from django.contrib.postgres.fields import ArrayField

class BookData(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    image=models.ImageField()
    url=models.URLField()
    originalPrice=models.CharField(max_length=50)
    salePrice=models.CharField(max_length=50)


def __str__(self):
    return self.title