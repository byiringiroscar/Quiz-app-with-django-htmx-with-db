from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional
from .models import Quiz

# Create your views here.



def start_quiz_view(request) -> HttpResponse:
  topics = Quiz.objects.all().annotate(questions_count=Count('question'))
  context = {
    'topics': topics
  }
  return render(
    request, 'start.html', context
  )