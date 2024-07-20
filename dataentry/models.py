from django.db import models

class Student(models.Model):
  roll_no = models.CharField(max_length=10)
  name = models.CharField(max_length=50)
  age = models.IntegerField()

  def __str__(self):
    return self.name


class Customer(models.Model):
  customer_name = models.CharField(max_length=25)
  country = models.CharField(max_length=25)

  def __str__(self):
    return self.customer_name
    



