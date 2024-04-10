from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

import random
from faker import Faker



class Command(BaseCommand):
    fake = Faker()
    
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)
    
    def handle(self, *args, **options):
        ratio = options["ratio"]
        self.fill_profiles(ratio)
        self.fill_tags(ratio)    
        self.fill_questions(10*ratio)
        self.fill_answers(100*ratio)
        self.fill_likes_questions(200*ratio)
        self.fill_likes_answers(200*ratio)
        
    
    def fill_profiles(self, count):
        for i in range(count):
            username = self.fake.user_name()
            email = self.fake.email()
            while username in Profile.objects.values_list("user__username", flat=True):
                username = username + str(random.randint(1, 10000))
            while email in Profile.objects.values_list("user__email", flat=True):
                email = email + str(random.randint(1, 10000))
            Profile.objects.create(
                user = User.objects.create_user(username, email, str(i)),
                avatar="static/images/avatar.jpg"
            )
        print("PROFILES: DONE")
    
    def fill_tags(self, count):
        for i in range(count):
            tag_name = self.fake.word()
            while tag_name in Tag.objects.values_list("name", flat=True):
                tag_name = tag_name + str(random.randint(1, 10000))
            Tag.objects.create(name=tag_name)
        print("TAGS: DONE")
            
    def fill_questions(self, count):
        tags = Tag.objects.all()
        authors = Profile.objects.all()
        for i in range(count):
            author = random.choice(authors)              
            question = Question.objects.create(
                author = author,
                title = self.fake.sentence(),
                text = self.fake.text(),
            )
            question_tags = [random.choice(tags) for j in range(random.randint(1, 3))]
            question.tags.set(Tag.objects.add_tags(question_tags))
            question.save()
        print("QUESTIONS: DONE")
                
    def fill_answers(self, count):
        authors = Profile.objects.all()
        questions = Question.objects.all()
        for i in range(count):
            author = random.choice(authors)
            question = random.choice(questions)
            answer = Answer.objects.create(
                text = self.fake.text(),
                is_correct = random.choice([True, False]),
                question = question,
                author = author,
            )
            question.answers_count += 1
            question.save()
        print("ANSWERS: DONE")
    
    def fill_likes_questions(self, count):
        authors = Profile.objects.all()
        questions = Question.objects.all()
        for i in range(count):
            author = random.choice(authors)
            question = random.choice(questions)
            
            question_like = QuestionLike.objects.create(
                is_like = random.choice([True, False]), 
                author = author,
                question = question,
            )
            
            if question_like.is_like == True:
                question.score += 1
                question.likes_count += 1
            else:
                question.score -= 1
                question.dislikes_count += 1
            question.save()
        print("LIKE QUESTIONS: DONE")
    
    def fill_likes_answers(self, count):
        authors = Profile.objects.all()
        answers = Answer.objects.all()
        for i in range(count):
            author = random.choice(authors)
            answer = random.choice(answers)
            answer_like = AnswerLike.objects.create(
                is_like = random.choice([True, False, True]), 
                author = author,
                answer = answer,
            )
            
            if answer_like.is_like == True:
                answer.score += 1
                answer.likes_count += 1
            else:
                answer.score -= 1
                answer.dislikes_count += 1
            answer.save()

        print("LIKE ANSWERS: DONE")