from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, AddForm
from .models import Challenge
from django.utils import timezone


def index(request):
    """ if request.user.is_authenticated():
        print("index: Kasutaja on sisse logitud!")
    else:
        print("index: Kasutaja EI OLE sisse logitud!") """

    select_challenge = Challenge.objects.filter(state=2)[:1]
    context = {'select_challenge': select_challenge}

    return render(request, 'WeekChallenge/index.html', context)


def about(request):
    return render(request, 'WeekChallenge/about.html')


def contact(request):
    return render(request, 'WeekChallenge/contact.html')


def add(request):
    if request.user.is_authenticated():
        add_form = AddForm()
        return render(request, 'WeekChallenge/add.html', {'add_form': add_form})
    else:
        return HttpResponseRedirect("/")


def add_challenge(request):
    if request.user.is_authenticated():
        title = request.POST['inputTitle']
        description = request.POST['inputDescription']
        # print(title, description, request.user, request.user.id)

        c = Challenge(title=title,
                      description=description,
                      username=request.user,
                      date=timezone.now(),
                      user_id=request.user.id)
        c.save()

        return HttpResponseRedirect("/add/")
    else:
        return HttpResponseRedirect("/")


def register(request):
    reg_form = RegisterForm()
    return render(request, 'WeekChallenge/register.html', {'form': reg_form})


def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        log_form = LoginForm()
        return render(request, 'WeekChallenge/login.html', {'form': log_form})


def my_profile(request):
    if request.user.is_authenticated():
        return render(request, 'WeekChallenge/my_profile.html')
    else:
        return HttpResponseRedirect("/")


def check_challenges(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            challenge_list = Challenge.objects.filter(state=0)[:10]
            accepted_list = Challenge.objects.filter(state=1)[:10]
            this_week = Challenge.objects.filter(state=2)
            history_list = Challenge.objects.filter(state=3)

            context = {'challenge_list': challenge_list,
                       'accepted_list': accepted_list,
                       'history_list': history_list,
                       'this_week': this_week
                       }
            return render(request, 'WeekChallenge/check.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def accept_challenge(request, challenge_id):
    if request.user.is_authenticated():
        if request.user.is_staff:
            select_one = Challenge.objects.get(id=challenge_id)
            select_one.state = 1
            select_one.save()

            return HttpResponseRedirect("/check/")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def decline_challenge(request, challenge_id):
    if request.user.is_authenticated():
        if request.user.is_staff:
            select_one = Challenge.objects.get(id=challenge_id)
            select_one.state = 4
            select_one.save()

            return HttpResponseRedirect("/check/")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def create_user(request):
    if request.user.is_authenticated():
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
    else:
        return HttpResponseRedirect("/")


def auth(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
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
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
