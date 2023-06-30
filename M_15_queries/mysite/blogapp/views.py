from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ListArticlesView(ListView):
    model = Article
    template_name = 'blogapp/article_list.html'
    queryset = Article.objects.select_related(
        'author',
        'category',
    ).prefetch_related('tags').defer('author__bio', 'content')
    context_object_name = 'articles'