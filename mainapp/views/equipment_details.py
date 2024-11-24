from django.shortcuts import render, get_object_or_404
from mainapp.models import Contract, Equipment

def equipment_details(request, contract_number):
    # Obtener el contrato por su número
    contract = get_object_or_404(Contract, contract_number=contract_number)

    # Obtener los equipos asociados a ese contrato
    equipments = Equipment.objects.filter(contract=contract)

    # Contexto para pasar a la plantilla
    context = {
        'contract': contract,
        'equipments': equipments
    }
    
    return render(request, 'equipment_details.html', context)
