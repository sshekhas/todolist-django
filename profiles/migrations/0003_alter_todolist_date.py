# Generated by Django 4.2.1 on 2023-05-23 00:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_todolist_priority_todolist_is_urgent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
