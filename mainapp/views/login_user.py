from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from mainapp.models import UserAccount

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserAccount.objects.get(username=username)
            if check_password(password, user.password_hash):
                request.session['user_id'] = user.user_id  # Guarda el usuario en sesión
                return redirect('dashboard')  # Redirige al dashboard
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except UserAccount.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')  # Devuelve la página de login
