from django.views import View
from django.shortcuts import redirect, render
from mainapp.models import Event
from mainapp.forms import EventForm
from pymongo import MongoClient
from django.conf import settings
from bson.objectid import ObjectId
from mainapp.forms import EventForm


class EventsView(View):
    def get(self, request):
        # Conectar a MongoDB
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        eventos_collection = db['events']

        # Obtener todos los documentos de la colección y convertir _id a string
        eventos = list(eventos_collection.find())
        for evento in eventos:
            evento['id'] = str(evento['_id'])
            # Eliminar el campo _id para evitar el error de plantilla
            del evento['_id']
        # Pasar los eventos a la plantilla
        client.close()
        return render(request, 'eventsList.html', {'eventos': eventos})

    def post(self, request):
        eventoId = request.POST.get('evento_id')
        evento_seleccionado = None
        if eventoId:
            evento_seleccionado = Event.objects.get(id=eventoId)
        eventosListados = Event.objects.all()
        return render(request, "crearEvento.html", {"eventos": eventosListados, "evento_seleccionado": evento_seleccionado})


class EventForm(View):
    form_class = EventForm
    initial = {"key": "value"}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, "eventForm.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            solicitud = form.cleaned_data

            client = MongoClient(settings.MONGO_URI)

            dbname = client.get_database('Proyecto_SID2')

            collection_name = dbname["events"]

            places_collection = dbname["locations"]
            place_id = solicitud.get('name')
            place_info = places_collection.find_one(
                {"_id": ObjectId(place_id)})

            event = {
                "title": solicitud.get('titulo'),
                "description": solicitud.get('descripcion'),
                "date": solicitud.get('fecha'),
                "place": place_info,
                "categories": solicitud.get('categoria').split(','),
            }
            collection_name.insert_one(event)
            client.close()
            return redirect("evento")

        return render(request, "eventForm.html", {"form": form})
