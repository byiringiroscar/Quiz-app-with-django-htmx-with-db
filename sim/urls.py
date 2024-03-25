from django.urls import path
from . import views

urlpatterns = [
  path('', views.start_quiz_view, name='start'),
]