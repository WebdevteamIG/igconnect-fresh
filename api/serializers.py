from django.db.models import fields
from rest_framework import serializers

from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'event', 'description', 'formLink', 'contactNumber', 'contactEmail', 'timestamp',
        )


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = (
            'id', 'event', 'rank', 'rankRange', 'desc', 'image',
        )


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = (
            'id', 'event', 'tag', 'fromtimestamp', 'totimestamp', 'desc', 'image',
        )

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = (
            'id', 'event', 'userName', 'userNumber', 'userEmail', 'timestamp',
        )




