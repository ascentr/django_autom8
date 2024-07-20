from django.core.management.base import BaseCommand, CommandError
#from dataentry.models import Student
from django.apps import apps
import csv

# python manage.py importdata  file_path model_name.

class Command(BaseCommand):
  help = "imports data from a CSV file on given file path"

  def add_arguments(self, parser):
    parser.add_argument('file_path', type=str, help="File Path to the CSV File")
    parser.add_argument('model_name', type=str, help="Name of the model") 
  
  def handle(self, *args, **kwargs):
    file_path = kwargs['file_path']
    model_name = kwargs['model_name'].capitalize()

    #search for the model across all installed apps using AppConfig.get_model(model_name, require_ready=True)¶
    model = None
    for app_config in apps.get_app_configs():
      try:
        model = apps.get_model(app_config.label, model_name)
        break # strop searching once the given model is found
      except LookupError:
        continue #i.e if model not found in current app continue searching in next app

    if not model:
      raise CommandError(f'Model {model_name} not found in any app')


    with open(file_path, 'r') as file:
      reader = csv.DictReader(file)

      for row in reader:
        model.objects.create(**row)

    self.stdout.write(self.style.SUCCESS("Data Inserted SUCCESSFULLY !!"))
          



