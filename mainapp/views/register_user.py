from django.shortcuts import render, redirect
from mainapp.forms import UserAccountCreationForm

def register_user(request):
    if request.method == 'POST':
        form = UserAccountCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guardamos el usuario en la base de datos
            return redirect('login')  # Redirigir al login
    else:
        form = UserAccountCreationForm()
    return render(request, 'register.html', {'form': form})
