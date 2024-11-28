# mainapp/management/commands/insert_data.py
from django.core.management.base import BaseCommand
from mainapp.models import Company, Contact, Department, ContactDepartment, Interaction, Opportunity, OpportunityStage, OpportunityStageHistory, ProductService, OpportunityProductService, Role, UserAccount, UserRole, Contract, Category, DeliveryCertificate, Equipment
from mainapp.models import MongoEquipment, LaptopAndDesktopSpecs, PrinterSpecs, TabletAndPhoneSpecs,ProjectorSpecs

class Command(BaseCommand):
    help = 'Insert data into PostgreSQL and MongoDB'

    def handle(self, *args, **kwargs):
        # Insertando datos en PostgreSQL

        # Insertando datos en MongoDB
        
        # Crear especificaciones de laptop y desktop
        laptop_specs = LaptopAndDesktopSpecs(
            processor="Intel i7",
            ram="16GB",
            storage_type="SSD",
            storage_capacity="512GB",
            graphics_card="NVIDIA GTX 1660",
            operating_system="Windows 10"
        )

        # Crear un equipo de laptop en MongoDB
        mongo_equipment_laptop = MongoEquipment(
            equipment_id="ME001",
            category="Laptop",
            laptop_and_desktop_specs=laptop_specs
        )
        mongo_equipment_laptop.save()

        projector_specs = ProjectorSpecs(
            resolution="1920x1080",
            brightness="3000 lumens",
            technology="DLP",
            lamp_life="5000 hours",
            aspect_ratio="16:9"
        )

        # Crear un equipo de proyector en MongoDB
        mongo_equipment_projector = MongoEquipment(
            equipment_id="ME002",
            category="Projector",
            projector_specs=projector_specs
        )

        mongo_equipment_projector.save()

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))