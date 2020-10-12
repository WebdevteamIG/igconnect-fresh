from django.contrib import admin

from .models import *

admin.site.register(Event)
admin.site.register(Timeline)
admin.site.register(Registration)
admin.site.register(Prize)