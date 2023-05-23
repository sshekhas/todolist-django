from django.db import models
from django.conf import settings
import datetime
from model_utils.models import TimeStampedModel


class TodoList(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30, help_text="title for the to do item")
    date = models.DateField(default=datetime.date.today)
    is_urgent = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    content = models.CharField(max_length=400, help_text="discription of todo list")
