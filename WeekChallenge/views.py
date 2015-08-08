from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from .models import Challenge


def index(request):
    """ if request.user.is_authenticated():
        print("index: Kasutaja on sisse logitud!")
    else:
        print("index: Kasutaja EI OLE sisse logitud!") """

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


def check_challenges(request):
    challenge_list = Challenge.objects.filter(state=0)[:10]
    accepted_list = Challenge.objects.filter(state=1)[:10]
    history_list = Challenge.objects.filter(state=3)

    context = {'challenge_list': challenge_list,
               'accepted_list': accepted_list,
               'history_list': history_list
               }
    return render(request, 'WeekChallenge/check.html', context)


def accept_challenge(request, challenge_id):
    select_one = Challenge.objects.get(id=challenge_id)
    select_one.state = 1
    select_one.save()

    return HttpResponseRedirect("/check/")


def decline_challenge(request, challenge_id):
    select_one = Challenge.objects.get(id=challenge_id)
    select_one.state = 4
    select_one.save()

    return HttpResponseRedirect("/check/")


def create_user(request):
    username = request.POST['inputUsername']
    email = request.POST['inputEmail']
    password = request.POST['inputPassword']
    firstname = request.POST['inputFirstName']
    lastname = request.POST['inputLastName']

    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    # Loging in
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            # print("auth: Success! Logged in!")
            return HttpResponseRedirect("/")
        else:
            # print("auth: Disabled account!")
            return HttpResponseRedirect("/")
    else:
        # print("auth: Wrong username and/or password!")
        return HttpResponseRedirect("/log_in/")


def auth(request):
    username = request.POST['inputUsername']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

            # print("auth: Success! Logged in!")
            return HttpResponseRedirect("/")
        else:
            # print("auth: Disabled account!")
            return HttpResponseRedirect("/")
    else:
        # print("auth: Wrong username and/or password!")
        return HttpResponseRedirect("/log_in/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")