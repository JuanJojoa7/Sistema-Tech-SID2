# mainapp/urls.py
from django.urls import path
from mainapp.views.dashboard import dashboard
from mainapp.views.equipment_details import equipment_details
from mainapp.views.home import home
from mainapp.views.login_user import login_user
from mainapp.views.logout import logout
from mainapp.views.new_rental import new_rental, request_contract
from mainapp.views.register_user import register_user

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register_user, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_rental/', new_rental, name='new_rental'),
    path('request_contract/<str:contract_id>/', request_contract, name='request_contract'),
    path('equipment_details/<str:contract_number>/', equipment_details, name='equipment_details'),
]
