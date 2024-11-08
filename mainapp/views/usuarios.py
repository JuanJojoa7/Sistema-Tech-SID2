from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from pymongo import MongoClient
from bson import ObjectId
from mainapp.forms import UserForm


class UserDetail(View):
    template_name = 'userInformation.html'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("id")  # Obtén el valor del parámetro "id"
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        collection = db['users']
        # Busca el usuario por su _id
        user = collection.find_one({"_id": user_id})
        client.close()
        if user:
            # Renderiza la información del usuario en tu plantilla HTML
            return render(request, self.template_name, {"user": user})
        else:
            return HttpResponse("Usuario no encontrado")


class UserForm(View):
    form_class = UserForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, "userForm.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            solicitud = form.cleaned_data
            # <process form cleaned data>
            client = MongoClient(settings.MONGO_URI)

            # First define the database name
            dbname = client.get_database('Proyecto_SID2')

            # Now get/create collection name
            collection = dbname["users"]
            cities_collection = dbname["cities"]
            ciudad_id = solicitud.get('ciudad')
            ciudad_info = cities_collection.find_one(
                {"_id": ObjectId(ciudad_id)})
            user = {
                "id": solicitud.get('id'),
                "userName": solicitud.get('nombreUsuario'),
                "completedName": solicitud.get('nombreCompleto'),
                "relationship": solicitud.get('tipoRelacion'),
                "email": solicitud.get('email'),
                "ciudad": ciudad_info,
            }
            collection.insert_one(user)
            client.close()
            return redirect("evento")

        return render(request, "userForm.html", {"form": form})

class AddUserToEvent(View):
    def get(self, request, *args, **kwargs):
        # Obtén los parámetros del URL
        id_evento = self.kwargs.get('event_id')
        id_usuario = self.kwargs.get('assistant_id')
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        eventos_collection = db['events']
        # Busca el evento por su ID
        evento = eventos_collection.find_one({'_id': ObjectId(id_evento)})

        if evento:
            print('Entreeeee!!!')
            # Verifica si el atributo 'asistants' existe
            if 'assistants' not in evento:
                evento['assistants'] = []  # Crea la lista si no existe

            # Agrega el id_usuario al array 'asistants'
            evento['assistants'].append(ObjectId(id_usuario))

            # Actualiza el evento en la base de datos
            eventos_collection.update_one({'_id': ObjectId(id_evento)}, {'$set': evento})
        
        url = reverse('evento_detalles', kwargs={'event_id': id_evento})
        return redirect(url)

class AddSpeakersToEvent(View):
    def get(self, request, *args, **kwargs):
        # Obtén los parámetros del URL
        id_evento = self.kwargs.get('event_id')
        id_usuario = self.kwargs.get('assistant_id')
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        eventos_collection = db['events']
        # Busca el evento por su ID
        evento = eventos_collection.find_one({'_id': ObjectId(id_evento)})

        if evento:
            # Verifica si el atributo 'asistants' existe
            if 'speakers' not in evento:
                evento['speakers'] = []  # Crea la lista si no existe

            # Agrega el id_usuario al array 'asistants'
            evento['speakers'].append(ObjectId(id_usuario))

            # Actualiza el evento en la base de datos
            eventos_collection.update_one({'_id': ObjectId(id_evento)}, {'$set': evento})
        
        url = reverse('evento_detalles', kwargs={'event_id': id_evento})
        return redirect(url)
    
class AddOrganizerToEvent(View):
    def get(self, request, *args, **kwargs):
        # Obtén los parámetros del URL
        id_evento = self.kwargs.get('event_id')
        id_programa = self.kwargs.get('program_id')
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        eventos_collection = db['events']
        # Busca el evento por su ID
        evento = eventos_collection.find_one({'_id': ObjectId(id_evento)})

        if evento:
            # Verifica si el atributo 'asistants' existe
            if 'organizers' not in evento:
                evento['organizers'] = []  # Crea la lista si no existe

            # Agrega el id_usuario al array 'asistants'
            evento['organizers'].append(ObjectId(id_programa))

            # Actualiza el evento en la base de datos
            eventos_collection.update_one({'_id': ObjectId(id_evento)}, {'$set': evento})
        
        url = reverse('evento_detalles', kwargs={'event_id': id_evento})
        return redirect(url)