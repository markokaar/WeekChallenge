from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, AddForm
from .models import Challenge, UserChallenge, UserFriend, Notification, Message, FriendRequest
from django.utils import timezone

notifications_count = 0


def notification_count(request):
    if request.user.is_authenticated():
        all_notifications = Notification.objects.filter(user_id=request.user.id, new=True)
        all_friend_requests = FriendRequest.objects.filter(user_to=request.user.id, state=0)

        global notifications_count

        notifications_count = 0
        for n in all_notifications:
            notifications_count += 1

        for n in all_friend_requests:
            notifications_count += 1
        return notifications_count


def index(request):
    """ if request.user.is_authenticated():
        print("index: Kasutaja on sisse logitud!")
    else:
        print("index: Kasutaja EI OLE sisse logitud!") """
    notification_count(request)

    select_challenge = Challenge.objects.get(state=2)
    chid = select_challenge.id

    # Active challenge accepting check
    if UserChallenge.objects.filter(challenge_id=chid, user_id=request.user.id):
        is_accepted = True
    else:
        is_accepted = False

    context = {'c': select_challenge, 'is_accepted': is_accepted, 'notifications_count': notifications_count}
    return render(request, 'WeekChallenge/index.html', context)


def about(request):
    notification_count(request)
    return render(request, 'WeekChallenge/about.html', {'notifications_count': notifications_count})


def contact(request):
    notification_count(request)
    users = User.objects.filter()
    return render(request, 'WeekChallenge/contact.html', {'users': users, 'notifications_count': notifications_count})


def add(request):
    if request.user.is_authenticated():
        notification_count(request)
        add_form = AddForm()
        return render(request, 'WeekChallenge/add.html', {'add_form': add_form, 'notifications_count': notifications_count})
    else:
        return HttpResponseRedirect("/")


def notifications(request):
    if request.user.is_authenticated():
        notification_count(request)
        friend_requests = FriendRequest.objects.filter(user_to=request.user.id, state=0)
        all_notifications = Notification.objects.filter(user_id=request.user.id)

        n = []
        for f in friend_requests:
            n.append(f.user_from)
        print("asd ")
        print(n)

        find_friends = User.objects.filter(id__in=n)

        return render(request, 'WeekChallenge/notifications.html', {'friend_requests': friend_requests,
                                                                    'all_notifications': all_notifications,
                                                                    'notifications_count': notifications_count,
                                                                    'find_friends': find_friends
                                                                    })
    else:
        return HttpResponseRedirect("/")


def mark_read(request, notification_id):
    if request.user.is_authenticated():
        select_notification = Notification.objects.get(id=notification_id, user_id=request.user.id)
        select_notification.new = False
        select_notification.save()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def mark_unread(request, notification_id):
    if request.user.is_authenticated():
        select_notification = Notification.objects.get(id=notification_id, user_id=request.user.id)
        select_notification.new = True
        select_notification.save()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def delete_notification(request, notification_id):
    if request.user.is_authenticated():
        select_notification = Notification.objects.get(user_id=request.user.id, id=notification_id)
        select_notification.delete()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def add_friend(request, friend_id):
    if request.user.is_authenticated():
        friend_request = FriendRequest(user_from=request.user.id,
                                       user_to=friend_id,
                                       date=timezone.now())
        friend_request.save()

        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def accept_friend(request, friend_id):
    if request.user.is_authenticated():
        # deleting from FriendRequest table
        friend_request = FriendRequest.objects.get(user_from=friend_id, user_to=request.user.id)
        friend_request.delete()

        # Sending notification to request sender.
        send_notification = Notification(user_id=friend_id,
                                         title=request.user.username + " accepted your friend request!",
                                         new=True
                                         )
        send_notification.save()

        # Adding user to friendlist
        select_user = UserFriend.objects.filter(user_id=request.user.id)

        # if user in friend table. Creating friend for first user
        if select_user:
            select_user = UserFriend.objects.get(user_id=request.user.id)
            select_user.friends += "," + friend_id
            select_user.save()
        else:
            create_friend = UserFriend.objects.create()
            create_friend.user_id = request.user.id
            create_friend.friends = friend_id
            create_friend.save()

        # Adding to other user friendlist
        select_user = UserFriend.objects.filter(user_id=friend_id)

        if select_user:
            select_user = UserFriend.objects.get(user_id=friend_id)
            select_user.friends += "," + str(request.user.id)
            select_user.save()
        else:
            create_friend = UserFriend.objects.create()
            create_friend.user_id = friend_id
            create_friend.friends = request.user.id
            create_friend.save()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def decline_friend(request, friend_id):
    if request.user.is_authenticated():
        select_request = FriendRequest.objects.get(user_from=friend_id, user_to=request.user.id)
        select_request.state = 2
        select_request.save()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def search(request):
    if request.user.is_authenticated():
        notification_count(request)
        return render(request, 'WeekChallenge/search.html', {'notifications_count': notifications_count})
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


def profile(request, user_name):
    if request.user.is_authenticated():
        notification_count(request)
        user_name2 = User.objects.get(username=user_name)
        ch = UserChallenge.objects.filter(user_id=user_name2.id)
        challenges = Challenge.objects.filter()

        # If there is no accepted challenges
        if not ch:
            no_accepted = True
        else:
            no_accepted = False

        return render(request, 'WeekChallenge/profile.html', {'user_name': user_name2,
                                                              'ch': ch,
                                                              'challenges': challenges,
                                                              'no_accepted': no_accepted,
                                                              'notifications_count': notifications_count
                                                              })
    else:
        return HttpResponseRedirect("/")


def user_accept_challenge(request):
    if request.user.is_authenticated():
        week_challenge = Challenge.objects.get(state=2)
        chid = week_challenge.id

        # If already accepted
        if not UserChallenge.objects.filter(challenge_id=chid, user_id=request.user.id):
            week_challenge.accept_count += 1
            week_challenge.save()

            c = UserChallenge(user_id=request.user.id,
                              challenge_id=week_challenge.id,
                              date=timezone.now())
            c.save()

            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def check_challenges(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            notification_count(request)

            challenge_list = Challenge.objects.filter(state=0)[:10]
            accepted_list = Challenge.objects.filter(state=1)[:10]
            this_week = Challenge.objects.filter(state=2)
            history_list = Challenge.objects.filter(state=3)

            context = {'challenge_list': challenge_list,
                       'accepted_list': accepted_list,
                       'history_list': history_list,
                       'this_week': this_week,
                       'notifications_count': notifications_count
                       }
            return render(request, 'WeekChallenge/check.html', context)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def up_challenge(request, challenge_id):
    if request.user.is_authenticated():
        if request.user.is_staff:
            # Take old challenge down
            old_challenge = Challenge.objects.get(state=2)
            old_challenge.state = 3
            old_challenge.save()

            # Upload new challenge
            new_challenge = Challenge.objects.get(id=challenge_id)
            new_challenge.state = 2
            new_challenge.save()

            return HttpResponseRedirect("/check/")
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


def friendlist(request, user_id):
    if request.user.is_authenticated():
        notification_count(request)
        select_friendlist = UserFriend.objects.filter(user_id=user_id)

        if select_friendlist:
            select_friendlist = UserFriend.objects.get(user_id=user_id)
            s = select_friendlist.friends
            userlist = s.split(',')

            """
            find_friends = User.objects.filter()
            for one in userlist:
                find_friends = User.objects.filter(id=one) """

            find_friends = User.objects.filter(id__in=userlist)

            return render(request, 'WeekChallenge/friendlist.html', {'friendlist': select_friendlist,
                                                                     'find_friends': find_friends,
                                                                     'notifications_count': notifications_count})
        else:
            return render(request, 'WeekChallenge/friendlist.html', {'notifications_count': notifications_count})
    else:
        return HttpResponseRedirect("/")


# Users stuff
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
