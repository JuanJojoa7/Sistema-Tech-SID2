from django.shortcuts import redirect

def logout(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')  # Redirige al login
