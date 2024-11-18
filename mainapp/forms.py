from django import forms
from .models import UserAccount, Role, UserRole
from django.contrib.auth.hashers import make_password  # Para encriptar la contraseña

class UserAccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    user_id = forms.CharField(max_length=20)  # Agregamos el campo user_id
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)  # Selección del rol desde la base de datos
    secret_password = forms.CharField(widget=forms.PasswordInput, required=False)  # Contraseña secreta solo si el rol es admin

    class Meta:
        model = UserAccount
        fields = ['user_id', 'username', 'password', 'email', 'company', 'role', 'secret_password']

    def clean(self):
        cleaned_data = super().clean()
        role_choice = cleaned_data.get('role')
        secret_password = cleaned_data.get('secret_password')

        # Validamos la contraseña secreta solo si el rol es admin
        if role_choice and role_choice.role_name == 'R1':  # Suponiendo que 'R1' es el rol de admin
            if not secret_password:  # Si la contraseña secreta está vacía, lanzamos un error
                raise forms.ValidationError('La contraseña secreta es obligatoria para los administradores.')

            if secret_password != 'miContraseñaSecreta':  # Verificamos la contraseña secreta
                raise forms.ValidationError('La contraseña secreta no es correcta.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password_hash = make_password(self.cleaned_data['password'])  # Hacemos hash de la contraseña
        
        # Asignamos el rol al usuario
        role_choice = self.cleaned_data['role']
        if role_choice.role_name == 'R1':  # Si es admin, aseguramos que la contraseña secreta sea correcta
            secret_password = self.cleaned_data['secret_password']
            if secret_password == 'miContraseñaSecreta':  # Solo asignamos el rol si la contraseña es correcta
                user.save()  # Guardamos el usuario
                user_role = UserRole(user=user, role=role_choice)
                user_role.save()
            else:
                raise forms.ValidationError('La contraseña secreta no es correcta.')
        else:
            user.save()  # Guardamos el usuario
            user_role = UserRole(user=user, role=role_choice)
            user_role.save()

        return user
