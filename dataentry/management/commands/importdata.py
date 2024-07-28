from django.core.management.base import BaseCommand
import csv
from dataentry.utils import check_csv_error

class Command(BaseCommand):
  help = "imports data from a CSV file on given file path"

  def add_arguments(self, parser):
    parser.add_argument('file_path', type=str, help="File Path to the CSV File")
    parser.add_argument('model_name', type=str, help="Name of the model") 
  
  def handle(self, *args, **kwargs):
    file_path = kwargs['file_path']
    model_name = kwargs['model_name'].capitalize()

    model = check_csv_error(file_path, model_name)

    with open(file_path, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        model.objects.create(**row)

    self.stdout.write(self.style.SUCCESS("Data Inserted SUCCESSFULLY !!"))
          



