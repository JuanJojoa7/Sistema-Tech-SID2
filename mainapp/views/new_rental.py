from django.shortcuts import render

def new_rental(request):
    if request.method == 'POST':
        # Lógica para manejar una nueva solicitud de alquiler
        pass

    # Lógica para mostrar los equipos disponibles
    return render(request, 'new_rental.html')
