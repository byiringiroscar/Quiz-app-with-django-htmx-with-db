from django.urls import path
from . import views

urlpatterns = [
  path('', views.start_quiz_view, name='start'),
  path('get-questions/start', views.get_questions, {'is_start': True}, name='get-questions'),
  path('get-questions', views.get_questions, {'is_start': False}, name='get-questions'),
]