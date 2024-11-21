from django.shortcuts import render, redirect
from mainapp.models import Contract, Equipment, DeliveryCertificate, UserAccount

def dashboard(request):
    user_id = request.session.get('user_id')  # Obtenemos el usuario logueado desde la sesión
    if not user_id:
        return redirect('login')  # Si no hay usuario logueado, redirige al login

    try:
        user = UserAccount.objects.get(user_id=user_id)  # Obtenemos el usuario desde la base de datos
        # Obtener los contratos asociados a la empresa del usuario logueado
        contracts = Contract.objects.filter(company=user.company)

        # Obtener las actas de entrega asociadas a los contratos del usuario
        active_certificates = DeliveryCertificate.objects.filter(contract__in=contracts)
        # Obtener los equipos activos asociados a esas actas de entrega
        active_equipments = Equipment.objects.filter(certificate__in=active_certificates, active=True)

        context = {
            'contracts': contracts,
            'equipments': active_equipments,
        }
        return render(request, 'dashboard.html', context)

    except UserAccount.DoesNotExist:
        # Si el usuario no existe, redirige al login
        return redirect('login')
