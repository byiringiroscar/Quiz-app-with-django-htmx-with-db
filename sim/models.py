from django.db import models

# Create your models here.



class Quiz(models.Model):
  name = models.CharField(max_length=300)
  date_time = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.name
