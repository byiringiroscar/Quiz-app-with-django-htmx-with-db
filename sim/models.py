from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Quiz(models.Model):
  name = models.CharField(max_length=250)
  date_time = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.name


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  text = models.CharField(max_length=250)

def __str__(self):
    return f'{self.quiz.name} - {self.text[:20]}'


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=250)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.question.text[:20]} - {self.text[:20]}'
  


class QuizCompletionAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.name} - {self.user}'
    


    def result_records_user(self):
        return ResultRecord.objects.filter(quiz_attempt=self, user=self.user).first()
    
    def get_total_questions(self):
        return Question.objects.filter(quiz=self.quiz).count()
    

    def get_percentage_score(self):
        total_questions = self.get_total_questions()
        score = self.result_records_user().score
        return int(score / total_questions * 100)


  

class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizCompletionAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quiz_attempt} - {self.question}'

class ResultRecord(models.Model):
    quiz_attempt = models.ForeignKey(QuizCompletionAttempt, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz_attempt.quiz} - {self.score}'
    
    def get_individual_result(self):
        return ResultIndividual.objects.filter(result_record=self)
       
    

class ResultIndividual(models.Model):
    result_record = models.ForeignKey(ResultRecord, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.CharField(max_length=250)
    question = models.TextField()
    answer = models.TextField()
    correct_answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.result_record} - {self.quiz} - {self.question[:20]}'
    



