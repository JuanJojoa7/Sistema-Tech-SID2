# mainapp/urls.py
from django.urls import path
from mainapp.views.home import home
from mainapp.views.login_user import login_user
from mainapp.views.register_user import register_user

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
]
