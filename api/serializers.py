from django.db.models import fields
from rest_framework import serializers

from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = (
            'id', 'username', 'email',
        )

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        # fields = (
        #     'id', 'event', 'userName', 'userNumber', 'userEmail',
        # )

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = '__all__'
        



