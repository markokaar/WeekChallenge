from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm


def index(request):
    if request.user.is_authenticated():
        print("index: Kasutaja on sisse logitud!")
    else:
        print("index: Kasutaja EI OLE sisse logitud!")

    return render(request, 'WeekChallenge/index.html')


def about(request):
    return render(request, 'WeekChallenge/about.html')


def contact(request):
    return render(request, 'WeekChallenge/contact.html')


def add(request):
    return render(request, 'WeekChallenge/add.html')


def register(request):
    reg_form = RegisterForm()
    return render(request, 'WeekChallenge/register.html', {'form': reg_form})


def log_in(request):
    log_form = LoginForm()
    return render(request, 'WeekChallenge/login.html', {'form': log_form})


def my_profile(request):
    return render(request, 'WeekChallenge/my_profile.html')


def create_user(request):
    user = User.objects.create_user('test4', 'test4@example.com', '0000')
    user.last_name = 'perekon4'
    user.save()
    return HttpResponseRedirect("/")


def auth(request):
    username = request.POST['inputUsername']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            print("auth: Success! Logged in!")
            return HttpResponseRedirect("/")
        else:
            print("auth: Disabled account!")
            return HttpResponseRedirect("/")
    else:
        print("auth: Wrong username and/or password!")
        return HttpResponseRedirect("/log_in/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")