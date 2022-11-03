import csv
import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView
from .models import User, BlogModel, FilesModel
from .forms import CustomUserCreationForm, BlogForm, UploadBlogForm


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'blog/registration.html'
    success_url = '/accounts/profile/edit/{id}'

    def form_valid(self, form):
        super(RegisterView, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())


class Login(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True
    next_page = '/accounts/profile/view/'

    def get_default_redirect_url(self):
        return resolve_url(f'{self.next_page}{self.request.user.pk}')


class Logout(LogoutView):
    next_page = '/login'


class UpdateProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'avatar', 'phone']
    template_name = 'blog/edit_profile.html'
    context_object_name = 'profile'
    success_url = '/accounts/profile/view/{id}'


class DetailProfileView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'blog/view_profile.html'


class BlogListView(ListView):
    model = BlogModel
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'


class BlogDetailView(DetailView):
    model = BlogModel
    template_name = 'blog/detail_blog.html'
    context_object_name = 'detail_blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = context['object'].photo.filter(blog=context['object'])
        context['photos'] = photos
        return context


class CreateBlogView(FormView):
    form_class = BlogForm
    template_name = 'blog/create_blog.html'
    success_url = '/blogs/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateBlogView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog = BlogModel.objects.create(user=self.request.user,
                                        description=form.cleaned_data['description'])
        files = self.request.FILES.getlist('photos')
        for photo in files:
            FilesModel.objects.create(blog=blog, file=photo)
        return redirect(self.get_success_url())


class UploadBlogFile(FormView):
    form_class = UploadBlogForm
    template_name = 'blog/upload_blog.html'
    success_url = '/blogs/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadBlogFile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        file = form.cleaned_data['file'].read()
        csv_str = file.decode('Windows-1251').split('\n')
        csv_reader = csv.reader(csv_str, delimiter=";", quotechar='"')
        with open('logs.log', 'w') as log:
            for row in csv_reader:
                try:
                    log.write(f'{type(row[1])}')
                    blog = BlogModel.objects.create(user=self.request.user,
                                                    description=row[0])
                    date = ''.join(row[1].split('.'))
                    date = datetime.datetime.strptime(date, "%d%m%Y")
                    blog.date_create = date
                    blog.save()
                except IndexError:
                    break

        return redirect(self.get_success_url())
