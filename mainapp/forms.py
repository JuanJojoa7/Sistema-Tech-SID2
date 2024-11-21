from django import forms
from .models import UserAccount, Role, UserRole
from django.contrib.auth.hashers import make_password  # Para encriptar la contraseña

class UserAccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    user_id = forms.CharField(max_length=20)

    class Meta:
        model = UserAccount
        fields = ['user_id', 'username', 'password', 'email']

    def save(self, commit=True):
        # Crear el usuario
        user = super().save(commit=False)
        user.password_hash = make_password(self.cleaned_data['password'])  # Encriptamos la contraseña
        if commit:
            user.save()

        # Asignar el rol automáticamente como R2 (cliente)
        role = Role.objects.get(role_id='R2')  # Asegúrate de que el rol 'R2' existe en la base de datos
        UserRole.objects.create(user=user, role=role)

        return user
