from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailForm
from .models import Subscriber
from .tasks import send_email_task

from dataentry.utils import send_email_notification
from django.conf import settings


def send_email(request):

  if request.method == "POST":
    email_form = EmailForm(request.POST, request.FILES)
    if email_form.is_valid():
      email_form = email_form.save()
      mail_subject = request.POST.get('subject')
      message = request.POST.get('body')
      email_list = request.POST.get('email_list')

      #Access the selected email list & Extract email address from Subscriber model
      email_list = email_form.email_list
      subscribers = Subscriber.objects.filter(email_list=email_list)
      to_email = [email.email_address for email in subscribers]

      if email_form.attachment:
        attachment = email_form.attachment.path
      else:
        attachment = None

      send_email_task.delay(mail_subject, message, to_email, attachment=attachment)

      messages.success(request, "Email sent successfully")
      return redirect('send_email')

    return
  else:
    email_form = EmailForm()
    context = {
      'email_form' : email_form
    }

    return render(request, "emails/send-email.html" , context)
