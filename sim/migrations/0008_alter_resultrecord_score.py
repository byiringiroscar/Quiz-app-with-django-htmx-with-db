# Generated by Django 5.0.3 on 2024-03-25 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0007_remove_resultrecord_is_correct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultrecord',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]