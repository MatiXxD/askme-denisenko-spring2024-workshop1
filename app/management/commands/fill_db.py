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
        # self.fill_profiles(ratio)
        # self.fill_tags(ratio)    
        # self.fill_questions(10*ratio)
        # self.fill_answers(100*ratio)
        # self.fill_likes_questions(18*ratio)
        self.fill_likes_answers(182*ratio)
        
        
    def fill_profiles(self, count):
        profiles = list()
        usernames = list()
        emails = list()
        for i in range(count):
            username = self.fake.user_name()
            email = self.fake.email()
            while username in usernames:
                username = username + str(random.randint(1, 10000))
            while email in emails:
                email = email + str(random.randint(1, 10000))
            profile = Profile(
                user = User.objects.create_user(username, email, str(i)),
                avatar="static/images/avatar.jpg"
            )
            profiles.append(profile)
            usernames.append(username)
            emails.append(email)
        Profile.objects.bulk_create(profiles, batch_size=100)
        print("PROFILES: DONE")
    
    
    def fill_tags(self, count):
        tags = list()
        tags_names = list()
        for i in range(count):
            tag_name = self.fake.word()
            while tag_name in tags_names:
                tag_name = tag_name + "_" + str(random.randint(1, 10000))
            tags_names.append(tag_name)
            tags.append(Tag(name=tag_name))
        Tag.objects.bulk_create(tags, batch_size=100)
        print("TAGS: DONE")
            
            
    def fill_questions(self, count):
        tags = Tag.objects.all()
        authors = Profile.objects.all()
        questions = list()
        for i in range(count):
            author = random.choice(authors)              
            question = Question(
                author = author,
                title = self.fake.sentence(),
                text = self.fake.text(),
            )
            questions.append(question)
        Question.objects.bulk_create(questions, batch_size=100)
        
        for question in Question.objects.all():
            question_tags = [random.choice(tags) for j in range(random.randint(1, 3))]
            question.tags.set(Tag.objects.add_tags(question_tags))
            question.save()
        print("QUESTIONS: DONE")
            
                
    def fill_answers(self, count):
        authors = Profile.objects.all()
        questions = Question.objects.all()
        answers = list()
        for i in range(count):
            author = random.choice(authors)
            question = random.choice(questions)
            answer = Answer(
                text = self.fake.text(),
                is_correct = random.choice([True, False]),
                question = question,
                author = author,
            )
            question.answers_count += 1
            question.save()
            answers.append(answer)
        Answer.objects.bulk_create(answers, batch_size=100)
        print("ANSWERS: DONE")
    
    
    def fill_likes_questions(self, count):
        question_likes = list()
        iter = 0
        for author in Profile.objects.all():
            for question in Question.objects.all():
                
                if iter % 1000 == 0:
                    print(iter)
                
                question_like = QuestionLike(
                    is_like = random.choice([True, False, True]), 
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
                question_likes.append(question_like)
                
                if len(question_likes) >= 100000:
                    QuestionLike.objects.bulk_create(question_likes, batch_size=100)
                    question_likes.clear()

                
                iter += 1    
                if iter >= count: break
            if iter >= count: break
            
        QuestionLike.objects.bulk_create(question_likes, batch_size=100)
        print("LIKE QUESTIONS: DONE")
        
            
    def fill_likes_answers(self, count):
        
        answer_likes = list()
        iter = 0
        for author in Profile.objects.all():
            for answer in Answer.objects.all():
                
                if iter % 1000 == 0:
                    print(iter)
                
                answer_like = AnswerLike(
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
                answer_likes.append(answer_like) 
                
                if len(answer_likes) >= 100000:
                    AnswerLike.objects.bulk_create(answer_likes, batch_size=100)
                    answer_likes.clear()
                
                iter += 1   
                if iter >= count: break
            if iter >= count: break
            
        AnswerLike.objects.bulk_create(answer_likes, batch_size=100)
        print("LIKE ANSWERS: DONE")