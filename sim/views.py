from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count
from django.core.paginator import Paginator
from typing import Optional

# Create your views here.



def start_quiz_view(request) -> HttpResponse:
  return render(
    request, 'start.html'
  )