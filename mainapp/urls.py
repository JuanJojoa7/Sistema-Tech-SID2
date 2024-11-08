from django.urls import path
from django.views.generic import RedirectView
from .views import views_home, viewsComment
from .views import *

urlpatterns = [
    path('', views_home.homeView, name='home'),

    path('eventos/', EventsView.as_view(), name='evento'),
    path('crear_evento/', EventForm.as_view(), name='crear_evento'),
    path("usuario/<str:id>/", UserDetail.as_view(), name="usuario_detalles"),
    path('evento/<str:event_id>/',
         EventDetailView.as_view(), name='evento_detalles'),
    path('lugar_evento/', EventLocationView.as_view(), name='lugar_evento'),
    path('crear_usuario/', UserForm.as_view(), name='crear_usuario'),

    path('añadir_comentario/<str:event_id>/',
         CommentView.as_view(), name='añadir_comentario'),

    path('anadir_asistente/<str:event_id>/<str:assistant_id>/',
         AddUserToEvent.as_view(), name='anadir_asistente'),

    path('anadir_conferencista/<str:event_id>/<str:assistant_id>/',
         AddSpeakersToEvent.as_view(), name='anadir_conferencista'),
    
    path('anadir_organizador/<str:event_id>/<str:program_id>/',
         AddOrganizerToEvent.as_view(), name='anadir_organizador'),

]
