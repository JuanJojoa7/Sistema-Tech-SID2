from django.urls import path
from django.views.generic import RedirectView
from .views import views_home, viewsComment
from .views import *

urlpatterns = [
    path('', views_home.homeView, name='home')

]
