from django.shortcuts import render
from django.http import HttpResponse


def start_page(request, *args, **kwargs):
    return render(request, 'advertisements/start_page.html', {})


def python_basic(request, *args, **kwargs):
    return render(request, 'advertisements/python_basic.html', {})


def django_frame(request, *args, **kwargs):
    return render(request, 'advertisements/django_frame.html', {})


def java(request, *args, **kwargs):
    return render(request, 'advertisements/java.html', {})


def motion(request, *args, **kwargs):
    return render(request, 'advertisements/motion.html', {})


def web_layout(request, *args, **kwargs):
    return render(request, 'advertisements/weblayout.html', {})
