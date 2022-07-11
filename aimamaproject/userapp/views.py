from django.shortcuts import render
from .models import Profile
import requests


def index(request):
    context = {
        'posts': Profile.objects.order_by('-pk')
        if request.user.is_authenticated else []
    }
    return render(request, 'blog/index.html', context)
