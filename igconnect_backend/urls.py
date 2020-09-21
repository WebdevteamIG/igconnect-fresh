from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/_v1_/', include('api.urls')), # routes for the api
]
