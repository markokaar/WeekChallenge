from django.contrib import admin
from .models import Challenge, UserChallenge, UserFriend, Notification, Message, FriendRequest


admin.site.register(Challenge)
admin.site.register(UserChallenge)
admin.site.register(UserFriend)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(FriendRequest)
