from django.core.management import BaseCommand
from blogapp.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_list = [
            'Liric',
            'Prose',
            'Poetry',
        ]
        for category in category_list:
            Category.objects.create(name=category)