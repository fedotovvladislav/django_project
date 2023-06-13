from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import UserBioForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request,"requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm()
    }
    return render(request,"requestdataapp/user-bio-form.html", context)