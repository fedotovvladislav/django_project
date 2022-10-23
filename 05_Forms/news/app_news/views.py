from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from . import forms
from . import models


class CreateNews(View):

    def get(self, request):
        news_form = forms.NewsForm()

        return render(request, 'app_news/create_news.html', context={'news_form': news_form})

    def post(self, request):
        news_form = forms.NewsForm(request.POST)
        if news_form.is_valid():
            models.NewsModel.objects.create(**news_form.cleaned_data)
            return HttpResponseRedirect('/all_news')

        return render(request, 'app_news/create_news.html', context={'news_form': news_form})


class NewsListView(ListView):
    model = models.NewsModel
    template_name = 'app_news/all_news.html'
    context_object_name = 'news_list'


class NewsDetailView(DetailView):
    model = models.NewsModel
    template_name = 'app_news/detail_news.html'
    context_object_name = 'detail_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = context['object'].comments.filter(news=context['object'])
        comments_form = forms.CommentsForm()
        context['comments'] = comments
        context['comments_form'] = comments_form
        return context

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            form = {
                'user_name': request.user.username,
                'comment': request.POST['comment']
            }
            comments_form = forms.CommentsForm(form)
        else:
            comments_form = forms.CommentsForm(request.POST)
        if comments_form.is_valid():
            if request.user.is_authenticated:
                models.CommentsModel.objects.create(news=self.get_object(),
                                                    user=request.user,
                                                    **comments_form.cleaned_data)
            else:
                models.CommentsModel.objects.create(news=self.get_object(),
                                                    **comments_form.cleaned_data)
        return HttpResponseRedirect(f'/all_news/{self.get_object().id}')


class Login(LoginView):
    template_name = 'app_news/login.html'


class Logout(LogoutView):
    next_page = '/all_news'
