from django.urls import path
from . import views

urlpatterns = [
    path('importdata/', views.importdata, name="importdata"),
]
