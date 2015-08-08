from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


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
    return render(request, 'WeekChallenge/register.html')


def log_in(request):
    return render(request, 'WeekChallenge/login.html')


def my_profile(request):
    return render(request, 'WeekChallenge/my_profile.html')


def create_user(request):
    user = User.objects.create_user('test4', 'test4@example.com', '0000')
    user.last_name = 'perekon4'
    user.save()
    return HttpResponseRedirect("/")


def auth(request):
    """user = authenticate(username='test1', password='0000')
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
        else:
            print("The password is valid, bute the account has been disabled")
    else:
        print("The username and/or password were incorrect.")"""

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
        return HttpResponseRedirect("/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")