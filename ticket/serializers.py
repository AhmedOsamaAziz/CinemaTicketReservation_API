from dataclasses import field
from distutils.command.install import HAS_USER_SITE
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from .models import Guest, Movie, Reservation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservations', 'name', 'mobile']