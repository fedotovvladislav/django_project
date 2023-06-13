from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from timeit import default_timer


def shop_index(request: HttpRequest):
    context = {
        "time_running": default_timer(),
    }
    return render(request, 'newshop/shop-index.html', context=context)
