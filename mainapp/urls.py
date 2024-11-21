# mainapp/urls.py
from django.urls import path
from mainapp.views.dashboard import dashboard
from mainapp.views.home import home
from mainapp.views.login_user import login_user
from mainapp.views.new_rental import new_rental
from mainapp.views.register_user import register_user

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_rental/', new_rental, name='new_rental'),
]
