from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Test(models.Model):
    type_id = models.IntegerField(unique=True,default=0)
    name = models.CharField(max_length=100,default='Test')

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    # Add other fields for question metadata if needed

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    # Add fields for test metadata, like duration, passing score, etc.

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
