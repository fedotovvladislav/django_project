from django.db import models
from taggit.managers import TaggableManager


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40, db_index=True)


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='articles')
    tags = TaggableManager()
