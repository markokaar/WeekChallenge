from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^add/', views.add, name='add'),
    url(r'^register/', views.register, name='register'),
    url(r'^log_in/', views.log_in, name='log_in'),
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^auth/', views.auth, name='auth'),
    url(r'^log_out/', views.log_out, name='log_out'),
    url(r'^profile/(?P<user_name>[a-zA-Z0-9_.-]+)/$', views.profile, name='profile'),
    url(r'^check/', views.check_challenges, name='check_challenges'),
    url(r'^accept_challenge/(?P<challenge_id>[0-9]+)/$', views.accept_challenge, name='accept_challenge'),
    url(r'^decline_challenge/(?P<challenge_id>[0-9]+)/$', views.decline_challenge, name='decline_challenge'),
    url(r'^up_challenge/(?P<challenge_id>[0-9]+)/$', views.up_challenge, name='up_challenge'),
    url(r'^user_accept_challenge/', views.user_accept_challenge, name='user_accept_challenge'),
    url(r'^add_challenge/', views.add_challenge, name='add_challenge'),
    url(r'^notifications/', views.notifications, name='notifications'),
    url(r'^search/', views.search, name='search'),
    url(r'^add_friend/(?P<friend_id>[0-9]+)/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/(?P<friend_id>[0-9]+)/$', views.remove_friend, name='remove_friend'),
    url(r'^friendlist/(?P<user_id>[0-9]+)/$', views.friendlist, name='friendlist'),
    url(r'^accept_friend/(?P<friend_id>[0-9]+)/$', views.accept_friend, name='accept_friend'),
    url(r'^decline_friend/(?P<friend_id>[0-9]+)/$', views.decline_friend, name='decline_friend'),
    url(r'^mark_read/(?P<notification_id>[0-9]+)/$', views.mark_read, name='mark_read'),
    url(r'^mark_unread/(?P<notification_id>[0-9]+)/$', views.mark_unread, name='mark_unread'),
    url(r'^mark_read_pm/(?P<pm_id>[0-9]+)/$', views.mark_read_pm, name='mark_read_pm'),
    url(r'^mark_unread_pm/(?P<pm_id>[0-9]+)/$', views.mark_unread_pm, name='mark_unread_pm'),
    url(r'^delete_notification/(?P<notification_id>[0-9]+)/$', views.delete_notification, name='delete_notification'),
    url(r'^send_pm/', views.send_pm, name='send_pm'),
    url(r'^delete_pm/(?P<pm_id>[0-9]+)/$', views.delete_pm, name='delete_pm')
]
