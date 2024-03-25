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


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.question.text[:20]} - {self.text[:20]}'
  

class ResultRecord(models.Model):
    username = models.CharField(max_length=300)
    score = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.quiz} - {self.score}'
    

class ResultIndividual(models.Model):
    result_record = models.ForeignKey(ResultRecord, on_delete=models.CASCADE)
    quiz = models.CharField(max_length=300)
    question = models.TextField()
    answer = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return f'{self.result_record.username} - {self.quiz} - {self.question[:20]}'
