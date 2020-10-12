from rest_framework import serializers

from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration




