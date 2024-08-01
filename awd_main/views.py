from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .forms import RegisterationForm

from dataentry.tasks import celery_test_task


def home(request):
  return render(request, 'index.html')

def celery_test(request):
  celery_test_task.delay()
  return HttpResponse("<h3>Function Executed </h3>")

def register(request):
  if request.method == "POST":
    form = RegisterationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Registeration Successfull")
      return redirect('register')
    else:
      context = {'form':form}
      return render(request, 'register.html', context)
  else:
    form = RegisterationForm()
    context = {'form':form}

  return render(request, 'register.html', context)


def login(request):
  if request.method == "POST":
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = auth.authenticate(username=username, password=password)

      if user is not None:
        auth.login(request, user)
        return redirect('home')
      else:
        messages.error(request, 'Invalid Credentials')
        return redirect('login')
    else:
      context = { 'form':form }
      return render(request, 'login.html', context)
  else:
    form = AuthenticationForm()
    context = {'form' : form}

  return render(request, 'login.html' , context)


def logout(request):
  auth.logout(request)
  return redirect('home')