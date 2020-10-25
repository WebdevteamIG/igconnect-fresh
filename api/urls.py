from django.urls import path

from .views import *

urlpatterns = [
    path('', welcome, name="welcome"), #Tested
    path('user/', user, name = 'user'), 
    path('gettoken/', auth, name="auth"), #Tested
    path('getevents/', allevents, name="allevents"),#tested
    path('event/', event, name="event"), #Tested
    path('timeline/', timeline, name="timeline"), #Tested
    path('prize/', prize, name="prize"), #Tested
    path('registration/', registration, name="registration"), #Tested
]