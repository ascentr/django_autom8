import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import datetime

#propoed command python manage.py exportdata model_name --> file_path_name_stimestamp.csv 

class Command(BaseCommand):
  help = "Export data from student model to a csv file"

  def add_arguments(self, parser):
    parser.add_argument('model_name', type=str, help="Name of the model that holds the data")

  def handle(self, *args, **kwargs):
    model_name = kwargs['model_name'].capitalize()
    
    #search for model in all installed apps
    model = None
    for app_config in apps.get_app_configs():
      try:
        model = apps.get_model(app_config.label, model_name)
        break # break the for loop if model found
      except LookupError:
        continue #continue searching if model not found
    
    if model:
      data = model.objects.all()
      print([field.name for field in model._meta.get_fields()])    
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
      file_path = f'{model_name}_exported_data_{timestamp}.csv'

      with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([field.name for field in model._meta.get_fields()])

        for dt in data:
          writer.writerow([getattr(dt, field.name) for field in model._meta.get_fields()])

    else:
      self.stderr.write(self.style.ERROR(f'model {model_name} not found'))

    self.stdout.write(self.style.SUCCESS("Data Export Successfull"))
