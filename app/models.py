from django.db import models
from django.contrib.auth.models import User
from datetime import date



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    score = models.IntegerField(default=0)
    

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    answers_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField()
    score = models.IntegerField(default=0)
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    


class QuestionLike(models.Model):
    is_like = models.BooleanField()
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    is_like = models.BooleanField()
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
