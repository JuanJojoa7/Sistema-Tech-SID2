from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import Contract, Equipment, UserAccount

def new_rental(request):
    user_id = request.session.get('user_id')  # Obtener el usuario logueado
    if not user_id:
        return redirect('login')  # Redirigir al login si no hay sesión activa

    try:
        user = UserAccount.objects.get(user_id=user_id)

        # Obtener contratos que no están asignados al usuario
        contracts = Contract.objects.exclude(users=user)

        # Para cada contrato, buscar los equipos asociados
        contracts_with_equipments = []
        for contract in contracts:
            equipments = Equipment.objects.filter(contract=contract)
            contracts_with_equipments.append({
                'contract': contract,
                'equipments': equipments,
            })

        context = {
            'contracts_with_equipments': contracts_with_equipments,
        }
        return render(request, 'new_rental.html', context)

    except UserAccount.DoesNotExist:
        return redirect('login')

def request_contract(request, contract_id):
    user_id = request.session.get('user_id')  # Obtener el usuario logueado
    if not user_id:
        return redirect('login')  # Redirigir al login si no hay sesión activa

    try:
        # Asociar el contrato al usuario logueado
        contract = Contract.objects.get(contract_number=contract_id)
        user = UserAccount.objects.get(user_id=user_id)
        contract.users.add(user)  # Usamos 'add' en lugar de asignar directamente
        contract.save()

        messages.success(request, f"Contract {contract_id} has been successfully assigned.")
        return redirect('dashboard')  # Redirigir al dashboard

    except Contract.DoesNotExist:
        messages.error(request, "The selected contract is not available.")
        return redirect('new_rental')

    except UserAccount.DoesNotExist:
        return redirect('login')
