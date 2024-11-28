from django.shortcuts import render, get_object_or_404
from mainapp.models import Contract, Equipment as SQLEquipment
from mainapp.models import MongoEquipment
from bson import ObjectId


def equipment_details(request, contract_number):
    # Obtener el contrato por su número
    contract = get_object_or_404(Contract, contract_number=contract_number)

    # Obtener los equipos asociados al contrato desde SQL
    sql_equipments = SQLEquipment.objects.filter(contract=contract)

    # Crear una lista para almacenar equipos con sus detalles combinados
    associated_equipments = []

    for sql_equipment in sql_equipments:
        # Intentar obtener los detalles de MongoDB usando el ID de MongoDB almacenado en SQL
        mongo_detail = None
        if sql_equipment.mongo_document_id:
            try:
                mongo_detail = MongoEquipment.objects.get(id=ObjectId(sql_equipment.mongo_document_id))
            except (MongoEquipment.DoesNotExist, ValueError):
                # Manejar el caso donde el documento de MongoDB no existe o el ID no es válido
                pass
        
        # Agregar el equipo SQL y su detalle de MongoDB (si existe) a la lista
        associated_equipments.append({
            'sql_equipment': sql_equipment,
            'mongo_detail': mongo_detail
        })

    # Contexto para pasar a la plantilla
    context = {
        'contract': contract,
        'associated_equipments': associated_equipments
    }

    return render(request, 'equipment_details.html', context)
