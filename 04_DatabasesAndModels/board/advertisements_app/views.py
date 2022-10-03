from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Advertisement


class AdvertisementList(ListView):
    model = Advertisement
    template_name = 'advertisements_app/advertisements.html'
    context_object_name = 'advertisements_list'


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'advertisements_app/advertisement_detail.html'
    context_object_name = 'advertisement'