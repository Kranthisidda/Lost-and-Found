
from djongo import models
from django.utils import timezone
class User_Details(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)

from datetime import datetime

class Item_Details(models.Model):
    Types = [('lost', 'Lost'), ('found', 'Found')]
    username = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    branch = models.CharField(max_length=20)
    select_type = models.CharField(max_length=10, choices=Types)
    item_details = models.TextField(max_length=100, default="")
    time = models.CharField(max_length=20)

   


