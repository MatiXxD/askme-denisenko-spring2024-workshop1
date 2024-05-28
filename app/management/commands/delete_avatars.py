from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike


class Command(BaseCommand):
        
    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.avatar.delete()