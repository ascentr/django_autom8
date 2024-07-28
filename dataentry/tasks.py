import time
from awd_main.celery import app
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
  time.sleep(5)

  # send email
  mail_subject = "Test Subject"
  message = "This is a test email"
  to_email = settings.DEFAULT_TO_EMAIL
  send_email_notification(mail_subject, message, to_email)
  return 'Email Sent after 5s Delay -  Successfully'

@app.task
def import_data_task(file_path, model_name):
  try:
    call_command('importdata', file_path, model_name)
    message = "Your data was imported successfully"

  except Exception as e:
    message("There was an error! Data import failed")
    raise e

  # Notify user by email  
  mail_subject = "Data Import Status"
  to_email = settings.DEFAULT_TO_EMAIL
  send_email_notification(mail_subject, message, to_email)
  return ('Data Imported Successfully')

