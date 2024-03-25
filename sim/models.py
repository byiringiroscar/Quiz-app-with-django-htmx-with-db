from django.db import models

# Create your models here.



class Quiz(models.Model):
  name = models.CharField(max_length=300)
  date_time = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.name


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_answered  = models.BooleanField(default=False)


def __str__(self):
    return f'{self.quiz.name} - {self.text[:20]}'
