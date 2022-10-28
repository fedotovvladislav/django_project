from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from taggit.models import Tag
from . import forms
from . import models


class Register(View):

    def get(self, request):
        form = forms.CustomUserCreationForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, response):
        form = forms.CustomUserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(response, user)
            return redirect('/profile')
        else:
            return render(response, 'users/registration.html', {'form': form})


class Login(LoginView):
    template_name = 'users/login.html'
    next_page = '/all_news'


class Logout(LogoutView):
    next_page = '/all_news'


class NewsListView(ListView):
    model = models.NewsModel
    template_name = 'users/all_news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return models.NewsModel.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        if self.kwargs.get("slug"):
            context['title'] = f'Новости по тегу "{self.kwargs.get("slug")}"'
        else:
            context['title'] = 'Все новости'
        return context


# class TagListView(ListView):
#     template_name = 'users/all_news.html'
#     context_object_name = 'news_list'
#
#     def get_queryset(self):
#         return models.NewsModel.objects.filter(tags__slug=self.kwargs.get("slug")).all()
#
#     def get_context_data(self, **kwargs):
#         context = super(TagListView, self).get_context_data(**kwargs)
#         context['title'] = 'Новости по тегу'
#         return context


class NewsDetailView(DetailView):
    model = models.NewsModel
    template_name = 'users/detail_news.html'
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


class ProfileView(View):

    def get(self, request):
        form = forms.ProfileForm()
        return render(request, 'users/profile.html', {'form': form})

    def post(self, response):
        form = forms.ProfileForm(response.POST)
        if form.is_valid():
            user = response.user
            user.phone, user.city, user.email = form.cleaned_data.values()
            user.save()
            return redirect(f'/profile/{user.id}')
        return HttpResponseRedirect('/profile')


class ProfileDetailView(DetailView):
    model = models.User
    template_name = 'users/detail_profile.html'
    context_object_name = 'profile_detail'


class CreateNews(PermissionRequiredMixin, View):
    permission_required = 'app_users.add_newsmodel'

    def get(self, request):
        news_form = forms.NewsForm()
        return render(request, 'users/create_news.html', context={'news_form': news_form})

    def post(self, request):
        news_form = forms.NewsForm(request.POST)
        if news_form.is_valid():
            models.NewsModel.objects.create(**news_form.cleaned_data)
            news = models.NewsModel.objects.filter(
                name=news_form.cleaned_data['name'],
                description=news_form.cleaned_data['description']
            ).first()
            for tag in news_form.cleaned_data['tags']:
                news.tags.add(tag)
            return HttpResponseRedirect('/all_news')

        return render(request, 'users/create_news.html', context={'news_form': news_form})

class NewsUpdate(UpdateView):
    model = models.NewsModel
