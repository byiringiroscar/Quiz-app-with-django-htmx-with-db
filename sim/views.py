from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from .models import Quiz, Question, Answer, QuizCompletionAttempt, ResultRecord, ResultIndividual, QuestionAttempt
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
        question = _get_next_question(request, quiz_completion_attempt)
        if question is None:
            return get_finish(request, quiz_completion_attempt)
    
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
def _get_next_question(request, quiz_completion_attempt) -> Optional[Question]:
    quiz_id = request.POST['quiz_id']
    next_question = Question.objects.exclude(questionattempt__quiz_attempt=quiz_completion_attempt, questionattempt__is_answered=True).filter(quiz_id=quiz_id).first()
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
    QuestionAttempt.objects.create(
        quiz_attempt=quiz_complete_attempt,
        question=submitted_answer.question,
        is_answered=True
    )

    context={
      'submitted_answer': submitted_answer,
      'answer': correct_answer,
    }

    return render(request, 'partials/answer.html', context)


@login_required
def get_finish(request, quiz_completion_attempt) -> HttpResponse:
    quiz_completion_attempt.is_completed = True
    quiz_completion_attempt.save()
    question_count = Question.objects.filter(quiz=quiz_completion_attempt.quiz).count()
    score = ResultRecord.objects.get(quiz_attempt=quiz_completion_attempt).score
    percent = float(score / question_count) * 100
    percent = int(percent)
    context={
            'questions_count': question_count, 'score': score, 'percent_score': percent
        }
    return render(request, 'partials/finish.html', context) 



def handle_question_error(request) -> HttpResponse:
    return render(request, 'partials/error.html')