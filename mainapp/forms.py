from django import forms
from django.conf import settings
from pymongo import MongoClient


class EventForm(forms.Form):
    titulo = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=100)
    categoria = forms.CharField(
        max_length=100, label="Categoria (separada por , )")
    fecha = forms.DateInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = MongoClient(settings.MONGO_URI)
        dbname = client.get_database('Proyecto_SID2')
        collection = dbname["locations"]
        lugar = [(city["_id"], city["name"]) for city in collection.find()]
        self.fields["ciudad"] = forms.ChoiceField(choices=lugar, label="Lugar")
        client.close()

    widgets = {
        fecha: forms.DateInput(attrs={'class': 'form-control datepicker'}),
    }


class EventLocationForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre del Lugar")
    direccion = forms.CharField(widget=forms.Textarea, label="Dirección")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = MongoClient(settings.MONGO_URI)
        dbname = client.get_database('Proyecto_SID2')
        collection = dbname["cities"]
        cities = [(city["_id"], city["nombre"]) for city in collection.find()]
        self.fields["ciudad"] = forms.ChoiceField(
            choices=cities, label="Ciudad")
        client.close()


class UserForm(forms.Form):
    id = forms.CharField(max_length=100)
    nombreUsuario = forms.CharField(max_length=100, label='Nombre de Usuario')
    nombreCompleto = forms.CharField(max_length=100, label='Nombre Completo')
    tipoRelacion = forms.CharField(label='Tipo de realción', widget=forms.Select(
        choices=[('profesor', 'Profesor'), ('estudiante', 'Estudiante'), ('graduado', 'Graduado'), ('empresario', 'Empresario'), ('administrativo', 'Administrativo'), ('directivo', 'Directivo')]))
    email = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = MongoClient(settings.MONGO_URI)
        dbname = client.get_database('Proyecto_SID2')
        collection = dbname["cities"]
        cities = [(city["_id"], city["nombre"]) for city in collection.find()]
        self.fields["ciudad"] = forms.ChoiceField(
            choices=cities, label="Ciudad")
        client.close()


class CommentForm(forms.Form):
    comentario = forms.CharField(
        widget=forms.Textarea, label='Comentario', max_length=240)
    # Campo oculto para el ID del evento
    event_id = forms.CharField(widget=forms.HiddenInput())


class searchUser(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = MongoClient(settings.MONGO_URI)
        dbname = client.get_database('Proyecto_SID2')
        collection = dbname["users"]
        users = [(user["_id"], user["completedName"])
                 for user in collection.find()]
        self.fields["Nombre de usurio"] = forms.ChoiceField(
            choices=users, label="Nombre Completo")
        client.close()
