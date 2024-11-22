from django.db import models
import mongoengine
from mongoengine import *

# ------------------------Modelos de POSTGRESQL-------------------------------------------

class Company(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)

class Contact(models.Model):
    contact_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    last_interaction_date = models.DateField(blank=True, null=True)

class Department(models.Model):
    department_id = models.CharField(max_length=20, primary_key=True)
    department_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

class ContactDepartment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assignment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('contact', 'department')

class Interaction(models.Model):
    interaction_id = models.CharField(max_length=20, primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    interaction_date = models.DateField(auto_now_add=True)
    interaction_type = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class Opportunity(models.Model):
    opportunity_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL)
    opportunity_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    estimated_close_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='open')
    success_probability = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

class OpportunityStage(models.Model):
    stage_id = models.CharField(max_length=20, primary_key=True)
    stage_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

class OpportunityStageHistory(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    stage = models.ForeignKey(OpportunityStage, on_delete=models.CASCADE)
    change_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('opportunity', 'stage')

class ProductService(models.Model):
    product_service_id = models.CharField(max_length=20, primary_key=True)
    product_service_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='equipment_images/', null=True, blank=True)

class OpportunityProductService(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    product_service = models.ForeignKey(ProductService, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    negotiated_price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('opportunity', 'product_service')

class Role(models.Model):
    role_id = models.CharField(max_length=20, primary_key=True)
    role_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

class UserAccount(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

class UserRole(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

class Contract(models.Model):
    contract_number = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_value = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    users = models.ManyToManyField(UserAccount, related_name='contracts')  # Relación muchos a muchos

    def __str__(self):
        return f"Contrato {self.contract_number}"

class Category(models.Model):
    category_id = models.CharField(max_length=20, primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class DeliveryCertificate(models.Model):
    certificate_id = models.CharField(max_length=20, primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

class Equipment(models.Model):
    equipment_id = models.CharField(max_length=20, primary_key=True)
    inventory_code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    available_quantity = models.IntegerField(default=0)
    contract = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='equipment_images', null=True, blank=True)

    def __str__(self):
        return self.description

    # Campos específicos dependiendo del tipo de equipo
    processor = models.CharField(max_length=100, blank=True, null=True)
    ram = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    screen_size = models.FloatField(blank=True, null=True)
    battery_life = models.FloatField(blank=True, null=True)
    resolution = models.CharField(max_length=100, blank=True, null=True)


"""---------------------Modelos de Mongo-------------------"""


# class User(Document):
#     """
#     Modelo para representar los usuarios

#     Atributos:
#         username (CharField): Nombre de usuario.
#         fullName (CharField): Nombre descriptivo del usuario.
#         relationship (CharField): relación del usuario.
#         email (CharField): correo electronico del usuario.
#         city (CharField): ciudad del usuario.
#     """

#     username = StringField(
#         max_length=120
#     )

#     fullName = StringField(
#         max_length=240
#     )

#     relationship = StringField(
#         max_length=120
#     )

#     email = EmailField(
#         max_length=120
#     )

#     city_id = StringField(

#     )

#     def get_city(self):
#         city = City.objects.get(id=self.city_id)
#         return city


# class Comment(Document):
#     """
#     Modelo para representar los comentarios.

#     Atributos:
#         text (CharField): Texto del comentario.
#         userId (IntegerField): Identificador del usuario al cual pertenece el comentario.
#     """
#     text = StringField(
#         required=True
#     )

#     userId = ReferenceField(
#         User,
#         reverse_delete_rule=mongoengine.CASCADE
#     )


# class Category(Document):
#     """
#     Modelo para representar las categorías.

#     Atributos:
#         name (StringField): Nombre de la categoría.
#     """
#     name = StringField(
#         max_length=120
#     )


# class Faculty(Document):
#     """
#     Modelo para representar las facultades.

#     Atributos:
#         name (CharField): Nombre descriptivo de la facultad.
#     """
#     name = StringField(max_length=255)


# class Event(Document):
#     """
#     Modelo para representar los eventos

#     Atributos:
#         title (CharField): titulo descriptivo del evento.
#         description (CharField): descripción del evento.
#         categories (CharField): categorias del evento.
#         date (CharField): fecha de realización del evento.
#         location (CharField): ubicación del evento.
#     """
#     title = StringField(
#         max_length=255
#     )

#     description = StringField(
#         max_length=512
#     )

#     categories = ListField(ReferenceField
#                            (Category,
#                             reverse_delete_rule=NULLIFY)
#                            )

#     date = DateTimeField(

#     )

#     location_id = StringField()

#     def get_location(self):
#         # Realiza una consulta a la base de datos de Oracle para obtener la ubicación
#         location = Location.objects.get(id=self.location_id)
#         return location


# class Program(Document):
#     """
#     Modelo para representar los programas académicos.

#     Atributos:
#         name (CharField): Nombre descriptivo del programa.
#         facultyId (IntegerField): Identificador único de la facultad a la que pertenece.
#     """
#     name = StringField(
#         max_length=255
#     )

#     facultyId = ReferenceField(
#         Faculty,
#         reverse_delete_rule=mongoengine.CASCADE
#     )
