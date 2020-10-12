from django.urls import path

from .views import *

urlpatterns = [
    path('/', welcome, name="welcome"),
    path('/event', event, name="event"),
    path('/timeline/<int:eventId>', timeline, name="timeline"),
    path('/prize/<int:eventId>', prize, name="prize"),
    path('/registration/<int:eventId>', registration, name="registration"),
    
]