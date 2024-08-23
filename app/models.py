from django.db import models
from django.contrib.auth.models import User
from datetime import date

import random


class ProfileManager(models.Manager):
    def popular_profiles(self, count=5):
        members = list()
        for profile in Profile.objects.all():
            rating = 0.7*Question.objects.get_rating(profile) + 0.3*Answer.objects.get_rating(profile) 
            members.append((rating, profile.user.username))
    
        members.sort(reverse=True)
        popular_members = list()
        for i in range(count):
            popular_members.append(members[i][1])
        
        return popular_members

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
    
    objects = ProfileManager()
    
    def __str__(self):
        return self.user.username
    

class TagManager(models.Manager):
    def popular_tags(self, count=20):
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
    def update_score(self, is_add, is_like, question):
        if is_add:
            if is_like:
                question.score += 1
                question.likes_count += 1
            else:
                question.score -= 1
                question.dislikes_count += 1
        else:
            if is_like:
                question.score -= 1
                question.likes_count -= 1
            else:
                question.score += 1
                question.dislikes_count -= 1
    
    def get_rating(self, user):
        user_questions = Question.objects.filter(author=user)
        
        rating = 0
        for question in user_questions:
            rating += 0.8 * question.likes_count + 0.2 * question.dislikes_count
        
        return rating    
    
    def liked_question(self, question, profile, is_like):
        if QuestionLike.objects.filter(question=question, author=profile).exists():
            question_like = QuestionLike.objects.get(question=question, author=profile)
            if question_like.is_like == is_like:
                self.update_score(False, question_like.is_like, question)
                question_like.delete()
            else:
                self.update_score(False, question_like.is_like, question)
                question_like.delete()
                question_like = QuestionLike.objects.create(question=question, author=profile, is_like=is_like)
                self.update_score(True, is_like, question)
        else:
            question_like = QuestionLike.objects.create(question=question, author=profile, is_like=is_like)
            self.update_score(True, is_like, question)
        question.save()
        return question
        
    
    def new_questions(self):
        return self.order_by("-created_at")
    
    def questions_by_tag(self, tag):
        questions = self.filter(tags__name=tag).order_by("-created_at")
        if not questions:
            raise Question.DoesNotExist
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
    def update_score(self, is_add, is_like, answer):
        if is_add:
            if is_like:
                answer.score += 1
                answer.likes_count += 1
            else:
                answer.score -= 1
                answer.dislikes_count += 1
        else:
            if is_like:
                answer.score -= 1
                answer.likes_count -= 1
            else:
                answer.score += 1
                answer.dislikes_count -= 1
    
    def get_rating(self, user):
        user_answers = Answer.objects.filter(author=user)
        
        rating = 0
        for answer in user_answers:
            rating += 0.8 * answer.likes_count + 0.2 * answer.dislikes_count
        
        return rating    
    
    
    def liked_answer(self, answer, profile, is_like):
        if AnswerLike.objects.filter(answer=answer, author=profile).exists():
            answer_like = AnswerLike.objects.get(answer=answer, author=profile)
            if answer_like.is_like == is_like:
                self.update_score(False, answer_like.is_like, answer)
                answer_like.delete()
            else:
                self.update_score(False, answer_like.is_like, answer)
                answer_like.delete()
                answer_like = AnswerLike.objects.create(answer=answer, author=profile, is_like=is_like)
                self.update_score(True, is_like, answer)
        else:
            answer_like = AnswerLike.objects.create(answer=answer, author=profile, is_like=is_like)
            self.update_score(True, is_like, answer)
        answer.save()
        return answer
    
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
    
    class Meta:
        unique_together = ["author", "question"]


class AnswerLike(models.Model):
    is_like = models.BooleanField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["author", "answer"]
