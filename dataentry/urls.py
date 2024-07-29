from django.urls import path
from . import views

urlpatterns = [
    path('importdata/', views.importdata, name="importdata"),
    path('exportdata/', views.exportdata, name="exportdata"),
]
