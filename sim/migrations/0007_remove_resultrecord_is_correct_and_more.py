# Generated by Django 5.0.3 on 2024-03-25 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0006_remove_resultrecord_username_resultrecord_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultrecord',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='resultindividual',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
