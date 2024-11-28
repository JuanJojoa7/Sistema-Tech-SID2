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
        exclude = ['mongo_document_id']  # Excluir el campo 'mongo_document_id' del formulario

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
                
                
                if mongo_equipment.category in ["Laptop", "Desktop"] and mongo_equipment.laptop_and_desktop_specs:
                    specs = mongo_equipment.laptop_and_desktop_specs
                    self.fields['processor'].initial = specs.processor
                    self.fields['ram'].initial = specs.ram
                    self.fields['storage_type'].initial = specs.storage_type
                    self.fields['storage_capacity'].initial = specs.storage_capacity
                    self.fields['graphics_card'].initial = specs.graphics_card
                    self.fields['operating_system'].initial = specs.operating_system
                
                elif mongo_equipment.category == "Printer" and mongo_equipment.printer_specs:
                    specs = mongo_equipment.printer_specs
                    self.fields['print_technology'].initial = specs.print_technology
                    self.fields['conectivity'].initial = specs.connectivity
                
                elif mongo_equipment.category in ["Tablet", "Phone"] and mongo_equipment.tablet_and_phone_specs:
                    specs = mongo_equipment.tablet_and_phone_specs
                    self.fields['screen_size'].initial = specs.screen_size
                    self.fields['battery_life'].initial = specs.battery_life
                    self.fields['camera_resolution'].initial = specs.camera_resolution
                
                elif mongo_equipment.category == "Projector" and mongo_equipment.projector_specs:
                    specs = mongo_equipment.projector_specs
                    self.fields['resolution'].initial = specs.resolution
                    self.fields['brightness'].initial = specs.brightness
                    self.fields['technology'].initial = specs.technology
                    self.fields['lamp_life'].initial = specs.lamp_life
                    self.fields['aspect_ratio'].initial = specs.aspect_ratio

            except MongoEquipment.DoesNotExist as e:
                print(f"Error retrieving MongoDB document: {e}")


    def save(self, commit=True):
        equipment = super().save(commit=False)
        categorytemp = Category.objects.get(category_id=equipment.category.category_id)

        
        normalized_category = categorytemp.category_name
        category_mapping = {
            'Laptops': 'Laptop',
            'Desktops': 'Desktop',
            'Phones': 'Phone',
            'Tablets': 'Tablet',
            'Projectors': 'Projector',
            'Printers': 'Printer'
        }
        normalized_category = category_mapping.get(normalized_category, normalized_category)

        try:
            
            try:
                mongo_equipment = MongoEquipment.objects.get(equipment_id=equipment.equipment_id)
            except MongoEquipment.DoesNotExist:
                mongo_equipment = MongoEquipment(
                    equipment_id=equipment.equipment_id, 
                    category=normalized_category
                )

            # Populate specs based on category
            if normalized_category in ["Laptop", "Desktop"]:
                mongo_equipment.laptop_and_desktop_specs = LaptopAndDesktopSpecs(
                    processor=self.cleaned_data.get('processor', ''),
                    ram=self.cleaned_data.get('ram', ''),
                    storage_type=self.cleaned_data.get('storage_type', ''),
                    storage_capacity=self.cleaned_data.get('storage_capacity', ''),
                    graphics_card=self.cleaned_data.get('graphics_card', ''),
                    operating_system=self.cleaned_data.get('operating_system', '')
                )
            elif normalized_category == "Printer":
                mongo_equipment.printer_specs = PrinterSpecs(
                    print_technology=self.cleaned_data.get('print_technology', ''),
                    connectivity=self.cleaned_data.get('conectivity', '')
                )
            elif normalized_category in ["Tablet", "Phone"]:
                mongo_equipment.tablet_and_phone_specs = TabletAndPhoneSpecs(
                    screen_size=float(self.cleaned_data.get('screen_size', 0)),
                    battery_life=float(self.cleaned_data.get('battery_life', 0)),
                    camera_resolution=self.cleaned_data.get('camera_resolution', ''),
                )
            elif normalized_category == "Projector":
                mongo_equipment.projector_specs = ProjectorSpecs(
                    resolution=self.cleaned_data.get('resolution', ''),
                    brightness=self.cleaned_data.get('brightness', ''),
                    technology=self.cleaned_data.get('technology', ''),
                    lamp_life=self.cleaned_data.get('lamp_life', ''),
                    aspect_ratio=self.cleaned_data.get('aspect_ratio', '')
                )


            try:
                mongo_equipment.save()
                print(f"MongoDB document saved successfully for {normalized_category}")
                
                if mongo_equipment.id:
                    equipment.mongo_document_id = str(mongo_equipment.id)
                else:
                    print(f"Warning: No MongoDB ID for {normalized_category}")

            except Exception as save_error:
                print(f"Error saving MongoDB document for {normalized_category}: {save_error}")
                
            if commit:
                equipment.save()

            return equipment

        except Exception as e:
            print(f"Unexpected error in equipment save: {e}")
            raise