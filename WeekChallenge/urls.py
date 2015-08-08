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
]