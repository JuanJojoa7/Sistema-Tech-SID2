from bson import ObjectId
from django.shortcuts import render, redirect
from django.views import View
from mainapp.forms import EventLocationForm
from pymongo import MongoClient
from django.conf import settings

class EventLocationView(View):
    form_class = EventLocationForm
    initial = {}
    template_name = "locationsForm.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            solicitud = form.cleaned_data

            # Conectar a MongoDB
            my_client = MongoClient(settings.MONGO_URI)
            dbname = my_client.get_database('Proyecto_SID2')
            collection_name = dbname["locations"]
            cities_collection = dbname["cities"]
            ciudad_id = solicitud.get('ciudad')
            ciudad_info = cities_collection.find_one({"_id": ObjectId(ciudad_id)})
            # Crear documento
            event_location = {
                "name": solicitud.get('nombre'),
                "adress": solicitud.get('direccion'),
                "city": ciudad_info,
            }
            collection_name.insert_one(event_location)

            return redirect("lugar_evento")

        return render(request, self.template_name, {"form": form})
