from django.shortcuts import render, redirect
from mainapp.models import Contract, Equipment, DeliveryCertificate, UserAccount

def dashboard(request):
    user_id = request.session.get('user_id')  # Obtén el ID del usuario logueado
    if not user_id:
        return redirect('login')  # Si no hay usuario logueado, redirige al login

    try:
        # Obtén el usuario logueado
        user = UserAccount.objects.get(user_id=user_id)

        # Obtén los contratos asociados al usuario logueado
        contracts = Contract.objects.filter(user_id=user_id)

        # Obtén los certificados de entrega relacionados a esos contratos
        delivery_certificates = DeliveryCertificate.objects.filter(contract__in=contracts)

        # Obtén los equipos activos relacionados a esos certificados
        active_equipments = Equipment.objects.filter(certificate__in=delivery_certificates, active=True)

        context = {
            'user': user,  # Pasa el usuario al contexto
            'contracts': contracts,
            'equipments': active_equipments,
        }
        return render(request, 'dashboard.html', context)

    except UserAccount.DoesNotExist:
        return redirect('login')
