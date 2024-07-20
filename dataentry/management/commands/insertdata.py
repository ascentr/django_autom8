from django.core.management import BaseCommand
from dataentry.models import Student

"""
Add data to the database using custom command
"""

class Command(BaseCommand):
  help = "Insert data to the data base"

  def handle(self, *args, **kwargs):

    dataset = [
      {'roll_no':1002, 'name':'Hassan', 'age':21},
      {'roll_no':1003, 'name':'John', 'age':20},
      {'roll_no':1006, 'name':'Smiley', 'age':23},     
      {'roll_no':1007, 'name':'Jose', 'age':19},
    ]

    for data in dataset:
      roll_no = data['roll_no']
      existing_record = Student.objects.filter(roll_no=roll_no).exists()

      if not existing_record:
        Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
        self.stdout.write(self.style.SUCCESS("Record inserted successfully"))
      else:
        self.stdout.write(self.style.WARNING(f'student with roll no {roll_no} already exists'))
        
    self.stdout.write(self.style.SUCCESS("Data insertion complete"))


  