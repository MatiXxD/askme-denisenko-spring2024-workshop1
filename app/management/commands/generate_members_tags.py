from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Profile, Tag
from django.core.cache import cache

class Command(BaseCommand):
        
    def handle(self, *args, **options):
        cache.set("popular_members", Profile.objects.popular_profiles(), 600)
        cache.set("popular_tags", Tag.objects.popular_tags(), 600)
        