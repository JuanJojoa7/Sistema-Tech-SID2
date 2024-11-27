from django import forms
from .models import UserAccount, Role, UserRole
from django.contrib.auth.hashers import make_password  # Para encriptar la contraseña
from django import forms
from .models import Equipment, Category
from mongoengine import connect, disconnect, connection
from .models import LaptopAndDesktopSpecs, PrinterSpecs, TabletAndPhoneSpecs, ProjectorSpecs, MongoEquipment

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
        role = Role.objects.get(role_id='R002')  # Asegúrate de que el rol 'R2' existe en la base de datos
        UserRole.objects.create(user=user, role=role)

        return user

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        exclude = ['mongo_document_id']  # Exclude mongo_document_id from the form

    processor = forms.CharField(required=False)
    ram = forms.CharField(required=False)
    storage_type = forms.CharField(required=False)
    storage_capacity = forms.CharField(required=False)
    graphics_card = forms.CharField(required=False)
    operating_system = forms.CharField(required=False)
    print_technology = forms.CharField(required=False)
    conectivity = forms.CharField(required=False)
    screen_size = forms.CharField(required=False)
    battery_life = forms.CharField(required=False)
    camera_resolution = forms.CharField(required=False)
    resolution = forms.CharField(required=False)
    brightness = forms.CharField(required=False)
    technology = forms.CharField(required=False)
    lamp_life = forms.CharField(required=False)
    aspect_ratio = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processor'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['ram'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['storage_type'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['storage_capacity'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['graphics_card'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['operating_system'].widget.attrs.update({'class': 'laptop-desktop-field'})
        self.fields['print_technology'].widget.attrs.update({'class': 'printer-field'})
        self.fields['conectivity'].widget.attrs.update({'class': 'printer-field'})
        self.fields['screen_size'].widget.attrs.update({'class': 'tablet-phone-field'})
        self.fields['battery_life'].widget.attrs.update({'class': 'tablet-phone-field'})
        self.fields['camera_resolution'].widget.attrs.update({'class': 'tablet-phone-field'})
        self.fields['resolution'].widget.attrs.update({'class': 'projector-field'})
        self.fields['brightness'].widget.attrs.update({'class': 'projector-field'})
        self.fields['technology'].widget.attrs.update({'class': 'projector-field'})
        self.fields['lamp_life'].widget.attrs.update({'class': 'projector-field'})
        self.fields['aspect_ratio'].widget.attrs.update({'class': 'projector-field'})

        if self.instance and self.instance.mongo_document_id:
            try:
                mongo_equipment = MongoEquipment.objects.get(id=self.instance.mongo_document_id)
                if mongo_equipment.laptop_and_desktop_specs:
                    self.fields['processor'].initial = mongo_equipment.laptop_and_desktop_specs.processor
                    self.fields['ram'].initial = mongo_equipment.laptop_and_desktop_specs.ram
                    self.fields['storage_type'].initial = mongo_equipment.laptop_and_desktop_specs.storage_type
                    self.fields['storage_capacity'].initial = mongo_equipment.laptop_and_desktop_specs.storage_capacity
                    self.fields['graphics_card'].initial = mongo_equipment.laptop_and_desktop_specs.graphics_card
                    self.fields['operating_system'].initial = mongo_equipment.laptop_and_desktop_specs.operating_system
                if mongo_equipment.printer_specs:
                    self.fields['print_technology'].initial = mongo_equipment.printer_specs.print_technology
                    self.fields['conectivity'].initial = mongo_equipment.printer_specs.conectivity
                if mongo_equipment.tablet_and_phone_specs:
                    self.fields['screen_size'].initial = mongo_equipment.tablet_and_phone_specs.screen_size
                    self.fields['battery_life'].initial = mongo_equipment.tablet_and_phone_specs.battery_life
                    self.fields['camera_resolution'].initial = mongo_equipment.tablet_and_phone_specs.camera_resolution
                    self.fields['operating_system'].initial = mongo_equipment.tablet_and_phone_specs.operating_system
                if mongo_equipment.projector_specs:
                    self.fields['resolution'].initial = mongo_equipment.projector_specs.resolution
                    self.fields['brightness'].initial = mongo_equipment.projector_specs.brightness
                    self.fields['technology'].initial = mongo_equipment.projector_specs.technology
                    self.fields['lamp_life'].initial = mongo_equipment.projector_specs.lamp_life
                    self.fields['aspect_ratio'].initial = mongo_equipment.projector_specs.aspect_ratio
            except MongoEquipment.DoesNotExist:
                pass


    def save(self, commit=True):
        equipment = super().save(commit=False)
        categorytemp = Category.objects.get(category_id=equipment.category.category_id)

        # Check if a connection already exists
        try:
            # Attempt to get the current connection
            conn = connection.get_connection()
        except:
            # If no connection exists, use the global connection from settings
            print("No existing connection. Using global MongoDB connection.")

        # Normalize category name
        normalized_category = categorytemp.category_name
        if normalized_category == 'Laptops':
            normalized_category = 'Laptop'
        elif normalized_category == 'Desktops':
            normalized_category = 'Desktop'
        elif normalized_category == 'Phones':
            normalized_category = 'Phone'
        elif normalized_category == 'Tablets':
            normalized_category = 'Tablet'

        # Check if an existing MongoDB document exists
        try:
            mongo_equipment = MongoEquipment.objects.get(equipment_id=equipment.equipment_id)
        except MongoEquipment.DoesNotExist:
            mongo_equipment = MongoEquipment(equipment_id=equipment.equipment_id, category=normalized_category)

        # Debug: Print all cleaned_data to see what's being passed
        print("Cleaned Data:", self.cleaned_data)

        try:
            if normalized_category in ["Laptop", "Desktop"]:
                mongo_equipment.laptop_and_desktop_specs = LaptopAndDesktopSpecs(
                    processor=self.cleaned_data['processor'],
                    ram=self.cleaned_data['ram'],
                    storage_type=self.cleaned_data['storage_type'],
                    storage_capacity=self.cleaned_data['storage_capacity'],
                    graphics_card=self.cleaned_data['graphics_card'],
                    operating_system=self.cleaned_data['operating_system']
                )
            elif normalized_category == "Printer":
                mongo_equipment.printer_specs = PrinterSpecs(
                    print_technology=self.cleaned_data['print_technology'],
                    conectivity=self.cleaned_data['conectivity']
                )
            elif normalized_category in ["Tablet", "Phone"]:
                mongo_equipment.tablet_and_phone_specs = TabletAndPhoneSpecs(
                    screen_size=self.cleaned_data['screen_size'],
                    battery_life=self.cleaned_data['battery_life'],
                    camera_resolution=self.cleaned_data['camera_resolution'],
                    operating_system=self.cleaned_data['operating_system']
                )
            elif normalized_category == "Projector":
                mongo_equipment.projector_specs = ProjectorSpecs(
                    resolution=self.cleaned_data['resolution'],
                    brightness=self.cleaned_data['brightness'],
                    technology=self.cleaned_data['technology'],
                    lamp_life=self.cleaned_data['lamp_life'],
                    aspect_ratio=self.cleaned_data['aspect_ratio']
                )
            
            try:
                mongo_equipment.save()
                print("MongoDB document saved successfully.")
            except Exception as e:
                print(f"Error saving MongoDB document: {e}")

            # Update PostgreSQL model with MongoDB document ID
            equipment.mongo_document_id = str(mongo_equipment.id)
            equipment.save()

            return equipment

        except Exception as e:
            print(f"Error saving MongoDB document: {e}")