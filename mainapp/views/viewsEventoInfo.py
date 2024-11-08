from django.views import View
from django.shortcuts import redirect, render
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId


from django.views import View
from django.shortcuts import redirect, render
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId


class EventDetailView(View):
    def get(self, request, event_id):
        # Conectar a MongoDB
        client = MongoClient(settings.MONGO_URI)
        db = client.get_database('Proyecto_SID2')
        eventos_collection = db['events']

        # Obtener el documento del evento usando ObjectId
        evento = eventos_collection.find_one({'_id': ObjectId(event_id)})
        users_collection = db['users']
        users = [{str("id"): user["_id"], str("completedName")                  : user["completedName"]} for user in users_collection.find()]
        if evento:
            evento['id'] = str(evento['_id'])
            # Eliminar el campo _id para evitar el error de plantilla
            del evento['_id']

            faculties_collection = db['faculties']
            faculties_documents = faculties_collection.find()
            programas = []
            for doc in faculties_documents:
                id_programas = doc.get("programs", [])
                for programa in id_programas:
                    programa_dic = {str("id"): programa["_id"], str("programa"): programa["nombre"]}
                    programas.append(programa_dic)

            user_ids = evento.get('speakers', [])
            speakers = [{str("nombreCompleto"): user["completedName"], str("relacion"): user["relationship"]}
                        for user in users_collection.find({'_id': {'$in': [ObjectId(id) for id in user_ids]}})]

            user_ids = evento.get('assistants', [])
            assistants = [{str("nombreCompleto"): user["completedName"], str("relacion"): user["relationship"]}
                          for user in users_collection.find({'_id': {'$in': [ObjectId(id) for id in user_ids]}})]

            # Obtener los comentarios asociados al evento
            comentarios_collection = db['comments']
            comentarios = list(comentarios_collection.find(
                {'event_id': ObjectId(event_id)}))
            
            #Nombre de los programas en las facultades que tiene un evento
            programs_ids = evento.get('faculties', [])
            programas_evento = [{str("nombre"): faculty["programs.name"]}
                    for faculty in faculties_collection.find({'programs._id': {'$in': [ObjectId(id) for id in programs_ids]}})]
                        
            print(programas_evento)

            return render(request, 'informEvent.html', {
                'titulo': evento.get('title', ''),
                'categorias': evento.get('categories', []),
                'fecha': evento.get('date', ''),
                'lugar': evento.get('lugar', ''),
                'descripcion': evento.get('description', ''),
                'programas_evento': programas_evento,
                'programas': programas,
                'conferencistas': speakers,
                'asistentes': assistants,
                'comentarios': comentarios,
                'users': users,
                'event_id': event_id,  # Asegúrate de pasar el event_id aquí
            })
        else:
            # Redirige a la lista de eventos si el evento no existe
            return redirect('evento')
