from django.db import models
from django.contrib.auth.models import User
from datetime import date

import random



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    

class TagManager(models.Manager):
    def popular_tags(self, count):
        return self.order_by("-score")[:count]
    
    def add_tags(self, tags):
        for tag in tags:
            tag.score += 1
            tag.save()
        return tags            

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    score = models.IntegerField(default=0)    

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-created_at")
    
    def questions_by_tag(self, tag):
        return self.filter(tags__name=tag).order_by("-created_at")
    
    def hot_questions(self):
        return self.order_by("-score")
    
    def question_by_id(self, question_id):
        return self.filter(id=question_id)[0]

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

    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def question_answers(self, question_id):
        return self.filter(question__id=question_id)

class Answer(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField()
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    objects = AnswerManager()

    def __str__(self):
        return f"{self.question.id}_{self.author.user.username}"


class QuestionLike(models.Model):
    is_like = models.BooleanField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    is_like = models.BooleanField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)