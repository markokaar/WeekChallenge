from django.template import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm, RegisterForm, AddForm, MessageForm, SearchForm, EditUsernameForm, \
    EditNameForm, EditEmailForm, EditPasswordForm, EditBioForm
from .models import Challenge, UserChallenge, UserFriend, Notification, Message, FriendRequest
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

notifications_count = 0


def notification_count(request):
    if request.user.is_authenticated():
        all_notifications = Notification.objects.filter(user_id=request.user.id, new=True)
        all_friend_requests = FriendRequest.objects.filter(user_to=request.user.id, state=0)
        all_messages = Message.objects.filter(user_to=request.user.id, new=True)

        global notifications_count

        notifications_count = 0
        for n in all_notifications:
            notifications_count += 1

        for n in all_friend_requests:
            notifications_count += 1

        for n in all_messages:
            notifications_count += 1

        return notifications_count


def index(request):
    notification_count(request)

    select_challenge = Challenge.objects.get(state=2)
    chid = select_challenge.id

    # asd
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
    return render(request, 'WeekChallenge/contact.html', {'users': users,
                                                          'notifications_count': notifications_count})


def ads(request):
    notification_count(request)

    return render(request, 'WeekChallenge/ads.html', {'notifications_count': notifications_count})


def donate(request):
    notification_count(request)
    return render(request, 'WeekChallenge/donate.html', {'notifications_count': notifications_count})


def report(request, user_id):
    return render(request, 'WeekChallenge/report.html')


def add(request):
    if request.user.is_authenticated():
        notification_count(request)
        add_form = AddForm()

        if request.COOKIES.get('alert') == 'challenge_submitted':
            context = {'add_form': add_form,
                       'notifications_count': notifications_count,
                       'alert': request.COOKIES.get('alert')}
        else:
            context = {'add_form': add_form,
                       'notifications_count': notifications_count}

        response = render(request, 'WeekChallenge/add.html', context)
        response.delete_cookie('alert')
        return response
    else:
        return HttpResponseRedirect("/")


def notifications(request):
    if request.user.is_authenticated():
        notification_count(request)
        friend_requests = FriendRequest.objects.order_by('-id').filter(user_to=request.user.id, state=0)
        all_notifications = Notification.objects.order_by('-id').filter(user_id=request.user.id)
        all_messages = Message.objects.order_by('-id').filter(user_to=request.user.id)

        n = []
        for f in friend_requests:
            n.append(f.user_from)

        for f in all_messages:
            n.append(f.user_from)

        find_friends = User.objects.filter(id__in=n)

        return render(request, 'WeekChallenge/notifications.html', {'friend_requests': friend_requests,
                                                                    'all_notifications': all_notifications,
                                                                    'notifications_count': notifications_count,
                                                                    'find_friends': find_friends,
                                                                    'all_messages': all_messages
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


def mark_read_pm(request, pm_id):
    if request.user.is_authenticated():
        select_pm = Message.objects.get(id=pm_id, user_to=request.user.id)
        select_pm.new = False
        select_pm.save()

        return HttpResponseRedirect("/notifications/")
    else:
        return HttpResponseRedirect("/")


def mark_unread_pm(request, pm_id):
    if request.user.is_authenticated():
        select_pm = Message.objects.get(id=pm_id, user_to=request.user.id)
        select_pm.new = True
        select_pm.save()

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

        select_friend = User.objects.get(id=friend_id)
        return HttpResponseRedirect("/profile/" + select_friend.username)
    else:
        return HttpResponseRedirect("/")


def remove_friend(request, friend_id):
    if request.user.is_authenticated():
        # Remove from logged user
        select_user1 = UserFriend.objects.get(user_id=request.user.id)


        friendlist = select_user1.friends
        friendlist = friendlist.split(",")
        friendlist.remove(friend_id)
        friendlist = ','.join(friendlist)

        if friendlist == "":
            select_user1.delete()
        else:
            select_user1.friends = friendlist
            select_user1.save()

        select_user2 = UserFriend.objects.get(user_id=friend_id)
        friendlist = select_user2.friends
        friendlist = friendlist.split(",")
        friendlist.remove(str(request.user.id))
        friendlist = ','.join(friendlist)

        if friendlist == "":
            select_user2.delete()
        else:
            select_user2.friends = friendlist
            select_user2.save()

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
        if request.method == 'POST':
            username = request.POST['inputUsername']
            firstname = request.POST['inputFirstName']
            lastname = request.POST['inputLastName']
            email = request.POST['inputEmail']

            search_results = User.objects.filter(username__icontains=username,
                                                 first_name__icontains=firstname,
                                                 last_name__icontains=lastname,
                                                 email__icontains=email
                                                 )[:50]
            search_count = 0
            for n in search_results:
                search_count += 1

            notification_count(request)
            search_form = SearchForm()
            return render(request, 'WeekChallenge/search.html', {'notifications_count': notifications_count,
                                                                 'search_form': search_form,
                                                                 'search_results': search_results,
                                                                 'search_count': search_count
                                                                 })
        else:
            # Search form
            notification_count(request)
            search_form = SearchForm()
            return render(request, 'WeekChallenge/search.html', {'notifications_count': notifications_count,
                                                                 'search_form': search_form
                                                                 })
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

        response = HttpResponseRedirect("/add/")
        response.set_cookie('alert', 'challenge_submitted')
        return response
    else:
        return HttpResponseRedirect("/")


def register(request):
    reg_form = RegisterForm()

    if request.COOKIES.get('alert'):
        context = {'form': reg_form, 'alert': request.COOKIES.get('alert')}
    else:
        context = {'form': reg_form}

    response = render(request, 'WeekChallenge/register.html', context)
    response.delete_cookie('alert')
    return response


def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        log_form = LoginForm()

        if request.COOKIES.get('error_name') == "wrong_name_password":
            context = {'form': log_form, 'error': request.COOKIES.get('error_name')}
        elif request.COOKIES.get('error_name') == "disabled":
            context = {'form': log_form, 'error': request.COOKIES.get('error_name')}
        else:
            context = {'form': log_form}

        response = render(request, 'WeekChallenge/login.html', context)
        response.delete_cookie('error_name')

        return response


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

        # Check if already friends
        already_friends = False
        check_friendship = UserFriend.objects.filter(user_id=request.user.id)
        if check_friendship:
            check_friendship = UserFriend.objects.get(user_id=request.user.id)
            # print(check_friendship.friends)
            s = check_friendship.friends
            userlist = s.split(',')
            userlist = list(map(int, userlist))

            if user_name2.id in userlist:
                already_friends = True

        # Check if request sent.
        request_sent = False
        check_request = FriendRequest.objects.filter(user_from=request.user.id, user_to=user_name2.id)
        if check_request:
            request_sent = True
        else:
            request_sent = False

        # IF profile belongs to logged user
        its_you = False
        if request.user.username == user_name:
            its_you = True

        # Private message stuff
        message_form = MessageForm()

        if request.COOKIES.get('alert'):
            context = {'user_name': user_name2,
                       'ch': ch,
                       'challenges': challenges,
                       'no_accepted': no_accepted,
                       'notifications_count': notifications_count,
                       'message_form': message_form,
                       'already_friends': already_friends,
                       'its_you': its_you,
                       'request_sent': request_sent,
                       'alert': request.COOKIES.get('alert')
                       }
        else:
            context = {'user_name': user_name2,
                       'ch': ch,
                       'challenges': challenges,
                       'no_accepted': no_accepted,
                       'notifications_count': notifications_count,
                       'message_form': message_form,
                       'already_friends': already_friends,
                       'its_you': its_you,
                       'request_sent': request_sent,
                       }

        response = render(request, 'WeekChallenge/profile.html', context)
        response.delete_cookie('alert')

        return response
    else:
        return HttpResponseRedirect("/")


def settings(request):
    if request.user.is_authenticated():
        notification_count(request)
        e_username_form = EditUsernameForm()
        e_name_form = EditNameForm()
        e_email_form = EditEmailForm()
        e_password_form = EditPasswordForm()
        e_bio_form = EditBioForm()

        return render(request, 'WeekChallenge/settings.html', {'e_username_form': e_username_form,
                                                               'e_name_form': e_name_form,
                                                               'e_email_form': e_email_form,
                                                               'e_password_form': e_password_form,
                                                               'e_bio_form': e_bio_form,
                                                               'notifications_count': notifications_count
                                                               })
    else:
        return HttpResponseRedirect("/")

"""
def upload_image(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

    return HttpResponseRedirect("/settings/")"""


def edit(request, typee):
    if request.user.is_authenticated():
        if request.method == "GET":

            if typee == "username":
                if not request.GET['inputUsername'] == "":
                    if not request.GET['inputPassword'] == "" and check_password(request.GET['inputPassword'], request.user.password):
                        if not User.objects.filter(username=request.GET['inputUsername']):
                            # Everything OK - username not empty, not in use, pw matches.
                            usern = User.objects.get(username=request.user.username)
                            usern.username = request.GET['inputUsername']
                            usern.save()
                        else:
                            print("username already in use!")
                            return HttpResponseRedirect("/settings/")
                    else:
                        print("pw is wrong")
                        return HttpResponseRedirect("/settings/")
                else:
                    print("No username!!")
                    return HttpResponseRedirect("/settings/")

            elif typee == "realname":
                usern = User.objects.get(username=request.user.username)
                usern.first_name = request.GET['inputFirstName']
                usern.last_name = request.GET['inputLastName']
                usern.save()

            elif typee == "email":
                if not request.GET['inputEmail'] == "" and not User.objects.filter(email=request.GET['inputEmail']):
                    usern = User.objects.get(username=request.user.username)
                    usern.email = request.GET['inputEmail']
                    usern.save()
                else:
                    print("Email empty or already in use")
                    return HttpResponseRedirect("/settings/")

            elif typee == "password":
                if not request.GET['inputPassword'] == "" and not request.GET['inputNewPassword'] == "" and not request.GET['inputNewPassword2'] == "":
                    if check_password(request.GET['inputPassword'], request.user.password):
                        if request.GET['inputNewPassword'] == request.GET['inputNewPassword2']:
                            new_pw = make_password(request.GET['inputNewPassword'])
                            usern = User.objects.get(username=request.user.username)
                            usern.password = new_pw
                            usern.save()

                            print("Password changed!")
                            return HttpResponseRedirect("/password_changed/")
                        else:
                            print("New passwords does not match")
                            return HttpResponseRedirect("/settings/")
                    else:
                        print("Old password is wrong!")
                        return HttpResponseRedirect("/settings/")
                else:
                    print("Something is missing.. Did you insert all 3 passwords?")
                    return HttpResponseRedirect("/settings/")
            elif typee == 'bio':
                new_bio = request.GET['inputBio']
                request.user.userprofile.bio = new_bio
                request.user.userprofile.save()

            else:
                print("wtf? Something happened..")

            return HttpResponseRedirect("/settings/")

        else:
            return HttpResponseRedirect("/settings/")
    else:
        return HttpResponseRedirect("/")


def password_changed(request):
    if request.user.is_authenticated():
        return render(request, 'WeekChallenge/password_changed.html')
    else:
        return HttpResponseRedirect("/")


def send_pm(request):
    if request.user.is_authenticated():
        pm_id = request.POST['pm_id']
        pm_title = request.POST['inputTitle']
        pm_content = request.POST['inputContent']

        pm_username = User.objects.get(id=pm_id)

        create_message = Message(user_to=pm_id,
                                 user_from=request.user.id,
                                 title=pm_title,
                                 content=pm_content,
                                 date=timezone.now()
                                 )
        create_message.save()
        response = HttpResponseRedirect("/profile/" + pm_username.username)
        response.set_cookie('alert', 'message_sent')
        return response
    else:
        return HttpResponseRedirect("/")


def delete_pm(request, pm_id):
    if request.user.is_authenticated():
        select_pm = Message.objects.get(id=pm_id, user_to=request.user.id)
        select_pm.delete()

        return HttpResponseRedirect("/notifications/")
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
        user_name = User.objects.get(id=user_id)

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
                                                                     'notifications_count': notifications_count,
                                                                     'user_name': user_name
                                                                     })
        else:
            return render(request, 'WeekChallenge/friendlist.html', {'notifications_count': notifications_count,
                                                                     'user_name': user_name})
    else:
        return HttpResponseRedirect("/")


# Users stuff
def create_user(request):
    if not request.user.is_authenticated():
        username = request.POST['inputUsername']
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']
        password2 = request.POST['inputPassword2']
        firstname = request.POST['inputFirstName']
        lastname = request.POST['inputLastName']

        response = HttpResponseRedirect("/register/")

        # Checking if everything is OK for creating user
        if not User.objects.filter(username=username):
            if len(username) > 3:
                if len(username) < 30:
                    try:
                        validate_email(email)
                    except ValidationError as e:
                        # print("Email not valid")
                        response.set_cookie('alert', 'email_not_valid')
                    else:
                        if len(password) > 5:
                            if len(password) < 50:
                                if password == password2:
                                    # Create user
                                    user = User.objects.create_user(username, email, password)
                                    user.first_name = firstname
                                    user.last_name = lastname
                                    user.save()

                                    # Loging in
                                    user = authenticate(username=username, password=password)
                                    if user is not None:
                                        if user.is_active:
                                            login(request, user)

                                            # print("auth: Success! Logged in! Something went wrong..")
                                            return HttpResponseRedirect("/")
                                        else:
                                            # print("auth: Disabled account! Something went wrong")
                                            return HttpResponseRedirect("/")
                                    else:
                                        # print("auth: Wrong username and/or password! -Something went really wrong..")
                                        return HttpResponseRedirect("/log_in/")
                                else:
                                    # print("passwords does not match.")
                                    response.set_cookie('alert', 'pw_not_matching')
                            else:
                                # print("Passwoord too long. more than 50 char")
                                response.set_cookie('alert', 'pw_long')
                        else:
                            # print("Password shorter than 5 characters")
                            response.set_cookie('alert', 'pw_short')
                else:
                    # print("Username too long. More than 30 char.")
                    response.set_cookie('alert', 'username_long')
            else:
                # print("username less than 3 characters")
                response.set_cookie('alert', 'username_short')
        else:
            # print("Username already in use")
            response.set_cookie('alert', 'username_in_use')

        return response
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
                response = HttpResponseRedirect("/log_in/")
                response.set_cookie('error_name', 'disabled')
                return response
        else:
            # print("auth: Wrong username and/or password!")
            response = HttpResponseRedirect("/log_in/")
            response.set_cookie('error_name', 'wrong_name_password')
            return response


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
