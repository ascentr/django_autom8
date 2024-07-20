from django.core.management.base import BaseCommand

"""
proposed command / out put ==> python manage.py greetings {name}
"""

class Command(BaseCommand):
  help = "Greet the User"   #class level help text

  def add_arguments(self, parser):
    parser.add_argument('name', type=str, help='Specifies the name of the user') # function level help text


  def handle(self, *args, **kwargs):
    name = kwargs['name']
    greetings = f'Hi {name}, Good Morning' 
    self.stdout.write(self.style.SUCCESS(greetings))
