from django.core.management import BaseCommand

from blogapp.models import Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        author_list = [
            {
                'name': 'Pushkin',
                'bio': 'Pushkin@example.com',
            },
            {
                'name': 'Jane Doe',
                'bio': 'tugrp@example.com',
            },
            {
                'name': 'Jeremia',
                'bio': 'Jeremia@example.com',
            }
        ]

        for author in author_list:
            Author.objects.create(**author)