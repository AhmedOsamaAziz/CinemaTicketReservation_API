from tkinter import CASCADE
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken import Token
from django.conf import settings

class Movie(models.Model):
     hall = models.CharField(max_length=10)
     movie = models.CharField(max_length=50)
     date = models.DateField()

     def __str__(self):
         return self.movie

    
class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=20)

    def __str__(self):
         return self.name

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
         return self.guest.name
