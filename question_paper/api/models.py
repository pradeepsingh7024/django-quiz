from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

class QuestionPaper(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('SUBJECTIVE', 'Subjective'),
    ]
    paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)
    option4 = models.CharField(max_length=100, blank=True)
    correct_option = models.CharField(max_length=100, blank=True)

class Answer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True)
    is_correct = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
