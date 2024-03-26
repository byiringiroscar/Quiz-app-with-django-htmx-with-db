from django.contrib import admin
from .models import Quiz, Question, Answer, QuizCompletionAttempt, ResultRecord, ResultIndividual

# Register your models here.


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizCompletionAttempt)
admin.site.register(ResultRecord)
admin.site.register(ResultIndividual)

