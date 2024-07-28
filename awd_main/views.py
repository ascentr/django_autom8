from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task

def home(request):
  return render(request, 'index.html')

def celery_test(request):

  celery_test_task.delay()
  return HttpResponse("<h3>Function Executed </h3>")
