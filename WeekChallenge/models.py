from django.db import models


class Challenge(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=5000)
    user_id = models.IntegerField(default=0)
    username = models.CharField(max_length=75)
    state = models.IntegerField(default=0)
    accept_count = models.IntegerField(default=0)
    date = models.DateTimeField('date added')

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user_id = models.IntegerField(default=0)
    challenge_id = models.IntegerField(default=0)
    date = models.DateTimeField('date accepted')

    def __int__(self):
        return self.challenge_id


class UserFriend(models.Model):
    user_id = models.IntegerField(default=0)
    friends = models.CommaSeparatedIntegerField(max_length=2000000000)

    def __int__(self):
        return self.user_id


class Notification(models.Model):
    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100000)
    new = models.BooleanField()

    def __str__(self):
        return self.title


class Message(models.Model):
    user_from = models.IntegerField(default=0)
    user_to = models.IntegerField(default=0)
    title = models.CharField(max_length=100000)
    content = models.TextField()
    date = models.DateTimeField('date sent')

