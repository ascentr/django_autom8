import time
from awd_main.celery import app
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification , generate_csv_file


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
  send_email_notification(mail_subject, message, [to_email])
  return ('Data Imported Successfully')


@app.task
def export_data_task(model_name):
  try:
    call_command('exportdata', model_name)
    message = "Your data was exported successfully - Plesae check the attachment file"
  except Exception as e:
    message = "There was an error data export failed"
    raise e

  #get file path for attachment file
  file_path = generate_csv_file(model_name)

  #attach csv file to email
  mail_subject = "Data Export Status"
  to_email = settings.DEFAULT_TO_EMAIL
  send_email_notification(mail_subject, message, [to_email], attachment=file_path)
  return ('Data Exported Successfully')


