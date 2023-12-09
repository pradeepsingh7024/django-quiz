from django.db import models

class Signup(models.Model):
    name=models.CharField(max_length=100)
    gmail=models.EmailField()
    password=models.CharField(max_length=100)
# Create your models here.
