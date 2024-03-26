# Generated by Django 5.0.3 on 2024-03-26 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0009_alter_answer_text_alter_question_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_answered',
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_answered', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sim.question')),
                ('quiz_attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sim.quizcompletionattempt')),
            ],
        ),
    ]