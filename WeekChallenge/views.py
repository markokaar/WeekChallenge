from django.shortcuts import render


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

