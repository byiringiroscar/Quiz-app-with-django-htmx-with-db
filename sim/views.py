from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from .models import Quiz, Question, Answer

# Create your views here.



def start_quiz_view(request) -> HttpResponse:
  topics = Quiz.objects.all().annotate(questions_count=Count('question'))
  context = {
    'topics': topics
  }
  return render(
    request, 'start.html', context
  )


def get_questions(request, is_start=False) -> HttpResponse:
    if is_start:
        username = 'Anonymous'
        question = _get_first_question(request)
    else:
        question = _get_next_question(request)
        if question is None:
            return render(request, 'partials/finish.html')
    
    answers = Answer.objects.filter(question=question)
    context = {
        'question': question,
        'answers': answers,
        'username': username
    }

    return render(request, 'partials/question.html', context)
        
    

def _get_first_question(request) -> Question:
  quiz_id = request.POST['quiz_id']
  return Question.objects.filter(quiz_id=quiz_id, is_answered=False).first()


def _get_next_question(request) -> Optional[Question]:
    quiz_id = request.POST['quiz_id']
    next_question = Question.objects.filter(quiz_id=quiz_id, is_answered=False).first()
    try:
        if next_question:
            return next_question
        return None
    except Question.DoesNotExist:
        return None
    


def get_answer(request) -> HttpResponse:
    submitted_answer_id = request.POST['answer_id']
    submitted_answer = Answer.objects.get(id=submitted_answer_id)
    submitted_answer.question.is_answered = True
    submitted_answer.question.save()

    if submitted_answer.is_correct:
        response = 'Correct!'