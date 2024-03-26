from django.urls import path
from . import views

urlpatterns = [
  path('', views.start_quiz_view, name='start'),
  path('get-questions/start/', views.get_questions, {'is_start': True}, name='get-questions'),
  path('get-questions/', views.get_questions, {'is_start': False}, name='get-questions'),
  path('get-answer/', views.get_answer, name='get-answer'),
  path('error/', views.handle_question_error, name='error'),
  path('view_records/', views.view_records, name='view_records'),

#   authentication routes
 path('signup/', views.signup_view, name='signup'),
 path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),

]