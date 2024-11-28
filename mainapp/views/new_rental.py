from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from mainapp.models import Contract, Equipment, UserAccount, Category

def new_rental(request):
    user_id = request.session.get('user_id')  # Obtener el usuario logueado
    if not user_id:
        return redirect('login')  # Redirigir al login si no hay sesión activa

    try:
        user = UserAccount.objects.get(user_id=user_id)

        # Obtener categorías para el filtro
        categories = Category.objects.all()

        # Filtros de categoría y búsqueda
        selected_category = request.GET.get('category', None)
        search_query = request.GET.get('search', '')

        contracts = Contract.objects.exclude(users=user)
        if selected_category:
            contracts = contracts.filter(
                equipment__category__category_id=selected_category
            ).distinct()

        if search_query:
            contracts = contracts.filter(
                Q(equipment__description__icontains=search_query) |
                Q(equipment__inventory_code__icontains=search_query)
            ).distinct()

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
            'categories': categories,
            'selected_category': selected_category,
            'search_query': search_query,
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
