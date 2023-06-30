from django.core.management import BaseCommand
from django.db.transaction import atomic

from blogapp.models import Author, Category, Article


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        author = Author.objects.get(pk=2)
        category = Category.objects.get(pk=2)
        article = Article.objects.create(
            title="Article title",
            content="Article text",
            author=author,
            category=category,
        )
        article.tags.add('tag1', 'tag2')
