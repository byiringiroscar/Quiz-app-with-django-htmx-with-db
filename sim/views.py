from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from .models import Quiz, Question, Answer, QuizCompletionAttempt, ResultRecord, ResultIndividual, QuestionAttempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.



def signup_view(request):
    if request.user.is_authenticated:
        return redirect('start')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # login user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('start')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('start')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('start')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def start_quiz_view(request) -> HttpResponse:
  user = request.user
  topics = Quiz.objects.all().annotate(questions_count=Count('question'))
  context = {
    'topics': topics,
    'user': user,
  }
  return render(
    request, 'start.html', context
  )

@login_required
def get_questions(request, is_start=False) -> HttpResponse:
    quiz_id = request.POST['quiz_id']
    if not quiz_id:
        return HttpResponseBadRequest('Please select a quiz topic.')
    quiz_completion_attempt, created = QuizCompletionAttempt.objects.get_or_create(
        quiz_id=quiz_id, user=request.user, is_completed=False
    )
    if not Question.objects.filter(quiz_id=quiz_id).exists():
        return handle_question_error(request)
    
    # Check if every question in the quiz has at least one answer
    questions_with_no_answers = Question.objects.filter(quiz_id=quiz_id).exclude(answer__isnull=False).distinct()
    if questions_with_no_answers.exists():
        return handle_question_error(request)
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
    if not submitted_answer_id:
        return HttpResponseBadRequest('Please select an answer.')
    submitted_answer = Answer.objects.get(id=submitted_answer_id)
    quiz = submitted_answer.question.quiz
    quiz_complete_attempt, created = QuizCompletionAttempt.objects.get_or_create(user=user, quiz=quiz, is_completed=False)
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


@login_required
def handle_question_error(request) -> HttpResponse:
    return render(request, 'partials/error.html')


@login_required
def view_records(request):
    user = request.user
    quiz_completion_attempts = QuizCompletionAttempt.objects.filter(user=user)
    context = {
        'quiz_completion_attempts': quiz_completion_attempts
    }
    return render(request, 'partials/records.html', context)