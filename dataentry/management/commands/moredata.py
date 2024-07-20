from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):

  def handle(self, *args, **kwargs):
    dataset = [
      {'roll_no':1008, 'name':'Hans', 'age':21},
      {'roll_no':1009, 'name':'Josh', 'age':20},
      {'roll_no':1006, 'name':'Smir', 'age':23},     
      {'roll_no':1005, 'name':'Yosef', 'age':19},
    ]

    for data in dataset:
      roll_no = data['roll_no']
      existing_record = Student.objects.filter(roll_no=roll_no).exists()
      if not existing_record:
        Student.objects.create(
          roll_no=data['roll_no'], name=data['name'], age=data['age'] 
          )
      else:
        self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists'))
    self.stdout.write(self.style.SUCCESS("Data Inserted Successfully"))
