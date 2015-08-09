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
    url(r'^my_profile/', views.my_profile, name='my_profile'),
    url(r'^check/', views.check_challenges, name='check_challenges'),
    url(r'^accept_challenge/(?P<challenge_id>[0-9]+)/$', views.accept_challenge, name='accept_challenge'),
    url(r'^decline_challenge/(?P<challenge_id>[0-9]+)/$', views.decline_challenge, name='decline_challenge'),
    url(r'^add_challenge/', views.add_challenge, name='add_challenge'),
]