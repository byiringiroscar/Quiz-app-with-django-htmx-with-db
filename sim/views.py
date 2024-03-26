from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from .models import Quiz, Question, Answer, QuizCompletionAttempt, ResultRecord, ResultIndividual
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def start_quiz_view(request) -> HttpResponse:
  topics = Quiz.objects.all().annotate(questions_count=Count('question'))
  context = {
    'topics': topics
  }
  return render(
    request, 'start.html', context
  )

@login_required
def get_questions(request, is_start=False) -> HttpResponse:
    quiz_id = request.POST['quiz_id']
    quiz_completion_attempt, created = QuizCompletionAttempt.objects.get_or_create(
        quiz_id=quiz_id, user=request.user, is_completed=False
    )
    if is_start:
        question = _get_first_question(request, quiz_completion_attempt)
    else:
        question = _get_next_question(request)
        if question is None:
            return render(request, 'partials/finish.html')
    
    answers = Answer.objects.filter(question=question)
    context = {
        'question': question,
        'answers': answers,
    }

    return render(request, 'partials/question.html', context)
        
    
@login_required
def _get_first_question(request, quiz_completion_attempt) -> Question:
  quiz_id = request.POST['quiz_id']
  return Question.objects.exclude(questionattempt__quiz_attempt=quiz_completion_attempt, questionattempt__is_answered=True).filter(quiz_id=quiz_id).first()

@login_required
def _get_next_question(request) -> Optional[Question]:
    quiz_id = request.POST['quiz_id']
    next_question = Question.objects.filter(quiz_id=quiz_id, is_answered=False).first()
    try:
        if next_question:
            return next_question
        return None
    except Question.DoesNotExist:
        return None
    

@login_required
def get_answer(request) -> HttpResponse:
    user = request.user
    submitted_answer_id = request.POST['answer_id']
    submitted_answer = Answer.objects.get(id=submitted_answer_id)
    quiz_complete_attempt, created = QuizCompletionAttempt.objects.get_or_create(user=user, is_completed=False)
    result_record, created = ResultRecord.objects.get_or_create(quiz_attempt=quiz_complete_attempt, user=user)
    answer_correct = False
    if submitted_answer.is_correct:
        correct_answer = submitted_answer
        result_record.score += 1
        result_record.save()
        answer_correct = True
    else:
        correct_answer = Answer.objects.get(
        question_id=submitted_answer.question_id, is_correct=True
        )
        answer_correct = False

    ResultIndividual.objects.create(
        result_record=result_record,
        quiz=submitted_answer.question.quiz.name,
        question=submitted_answer.question.text,
        answer=submitted_answer.text,
        correct_answer=correct_answer.text,
        is_correct=answer_correct,
    
    )

    context={
      'submitted_answer': submitted_answer,
      'answer': correct_answer,
    }

    return render(request, 'partials/answer.html', context)


