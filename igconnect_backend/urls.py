from django.contrib import admin
from django.urls import path, include

from ideasubmissionOIC.views import submission

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # routes for the api
    path('api/oic/idea/', submission, name="oicsubmissions"), # tested ok
]
