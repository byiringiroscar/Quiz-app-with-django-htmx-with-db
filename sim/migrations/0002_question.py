# Generated by Django 5.0.3 on 2024-03-25 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('is_answered', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sim.quiz')),
            ],
        ),
    ]
