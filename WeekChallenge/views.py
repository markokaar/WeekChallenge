from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, 'WeekChallenge/index.html')


def about(request):
    return render(request, 'WeekChallenge/about.html')


def contact(request):
    return render(request, 'WeekChallenge/contact.html')


def add(request):
    return render(request, 'WeekChallenge/add.html')


def register(request):
    return render(request, 'WeekChallenge/register.html')


def login(request):
    return render(request, 'WeekChallenge/login.html')


def auth(request):
    user = User.objects.create_user('test3', 'test3@example.com', '0000')
    user.last_name = 'perekon33d'
    user.save()
    return render(request, 'WeekChallenge/register.html')

