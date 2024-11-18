# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password  # Para verificar la contraseña
from mainapp.models import UserAccount

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = UserAccount.objects.get(username=username)  # Buscamos al usuario por su nombre de usuario
            if check_password(password, user.password_hash):  # Comparamos la contraseña encriptada
                # Si la contraseña es correcta, podemos iniciar sesión
                request.session['user_id'] = user.user_id  # Guardamos el ID del usuario en la sesión
                return redirect('dashboard')  # Redirige al dashboard
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except UserAccount.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
