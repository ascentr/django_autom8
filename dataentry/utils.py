from django.core.management.base import CommandError
from django.db import DataError
import os
import csv
import hashlib
import datetime
import time
from bs4 import BeautifulSoup
from django.core.mail import EmailMessage
from django.conf import settings
from django.apps import apps
from emails.models import Email, Sent , EmailTracking, Subscriber


# get all the models not system apps
def get_all_custom_models():

  default_models = [ 'LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'User', 'Upload' ]
  custom_models = []

  for model in apps.get_models():
    if model.__name__ not in default_models:
      custom_models.append(model.__name__)
  
  return custom_models


def check_csv_error(file_path, model_name):
  model = None

  # search for the model in all apps
  for app_config in apps.get_app_configs():
    try:
      model = apps.get_model(app_config.label, model_name)
      break # strop searching once the given model is found
    except LookupError:
      continue #i.e if model not found in current app continue searching in next app
  if not model:
    raise CommandError(f'Model {model_name} not found in any app')

  # Fetch model fields and corresponding csv headers
  if model:
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
  
  try:
    with open(file_path, 'r') as file:
      reader = csv.DictReader(file)
      csv_header = reader.fieldnames

      #compare csv headers with model_fields
      if csv_header != model_fields:
        raise DataError(f'CSV file does not math the {model_name} model fields')
  except Exception as e:
    raise e
  
  return model


def generate_csv_file(model_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    export_dir = 'exported_data'
    file_name = f'{model_name}_exported_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
  try:
    from_email = settings.DEFAULT_FROM_EMAIL
    for receipient_email in to_email:
      new_message = message
      #1- create email tracking record
      if email_id:
        email = Email.objects.get(pk=email_id)
        subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=receipient_email)
        email_list = email.email_list
        timestamp = str(time.time())
        data_to_hash = f'{receipient_email}{timestamp}'  
        unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
        email_tracking=EmailTracking.objects.create(
          email=email, 
          subscriber=subscriber,
          email_list=email_list,
          unique_id=unique_id,
        )

        #2- genereate the tracking url
        base_url = settings.BASE_URL
        click_tracking_url = f'{base_url}/emails/track/click/{unique_id}'
        open_tracking_url =f'{base_url}/emails/track/open/{unique_id}'

        #3- search for links in the email body
        soup = BeautifulSoup(message, 'html.parser')      
        urls = [a['href'] for a in soup.find_all('a', href=True)] 

        #4- if links in email body, inject click tracking url into the link
        if urls:
          for url in urls:
            tracking_url = f'{click_tracking_url}?url={url}'
            new_message = new_message.replace(f'{url}', f'{tracking_url}')
        else:
          print("NO URLs found in the message")

        #create email content with tracking pixel image
        open_tracking_image = f"<img src='{open_tracking_url}' width='1' height='1'>"
        new_message += open_tracking_image

      mail = EmailMessage(mail_subject, new_message, from_email, to=[receipient_email])
      if attachment is not None:
        mail.attach_file(attachment)
      
      mail.content_subtype = 'html'
      mail.send()

    #if sending email for the emails app use email_id to increment the total_sent count in the Sent model:
    if email_id:
      sent = Sent()
      sent.email = email
      sent.total_sent = email.email_list.count_emails()
      sent.save()

  except Exception as e:
    raise e



# def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
#   try:
#     from_email = settings.DEFAULT_FROM_EMAIL
#     mail = EmailMessage(mail_subject, message, from_email, to=to_email)
#     if attachment is not None:
#       mail.attach_file(attachment)
    
#     mail.content_subtype = 'html'
#     mail.send()

#     #if sending email for the emails app use email_id to increment the total_sent count in the Sent model:
#     if email_id:
#       email = Email.objects.get(pk=email_id)
#       sent = Sent()
#       sent.email = email
#       sent.total_sent = email.email_list.count_emails()
#       sent.save()

#   except Exception as e:
#     raise e


  