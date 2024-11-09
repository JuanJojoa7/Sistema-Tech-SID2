from django.db import models
import mongoengine
from mongoengine import *

""""------------------------Modelos de POSTGRESQL-------------------------------------------"""

# Tabla para representar la entidad Company
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Tabla para representar la entidad Shop
class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Tabla para representar la entidad City y Country
class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


# Tabla para representar la entidad Operational_Shop
class OperationalShop(models.Model):
    operational_shop_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Tabla para representar los horarios de las tiendas operativas
class OperationalShopHours(models.Model):
    operational_shop_hours_id = models.AutoField(primary_key=True)
    operational_shop = models.ForeignKey(OperationalShop, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()


# Tabla para almacenar los medios de las tiendas operativas
class OperationalShopMedia(models.Model):
    operational_shop_media_id = models.AutoField(primary_key=True)
    operational_shop = models.ForeignKey(OperationalShop, on_delete=models.CASCADE)
    media_url = models.URLField()


# Tabla para representar la entidad Product y Product_Stock
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductStock(models.Model):
    product_stock_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)


# Tabla para representar las monedas
class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=3)


# Tabla para representar contratos
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Contact, related_name='seller_contracts', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Contact, related_name='buyer_contracts', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Tabla para representar el estado de los contratos
class ContractStatus(models.Model):
    contract_status_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)


"""---------------------Modelos de Mongo-------------------"""


class User(Document):
    """
    Modelo para representar los usuarios

    Atributos:
        username (CharField): Nombre de usuario.
        fullName (CharField): Nombre descriptivo del usuario.
        relationship (CharField): relación del usuario.
        email (CharField): correo electronico del usuario.
        city (CharField): ciudad del usuario.
    """

    username = StringField(
        max_length=120
    )

    fullName = StringField(
        max_length=240
    )

    relationship = StringField(
        max_length=120
    )

    email = EmailField(
        max_length=120
    )

    city_id = StringField(

    )

    def get_city(self):
        city = City.objects.get(id=self.city_id)
        return city


class Comment(Document):
    """
    Modelo para representar los comentarios.

    Atributos:
        text (CharField): Texto del comentario.
        userId (IntegerField): Identificador del usuario al cual pertenece el comentario.
    """
    text = StringField(
        required=True
    )

    userId = ReferenceField(
        User,
        reverse_delete_rule=mongoengine.CASCADE
    )


class Category(Document):
    """
    Modelo para representar las categorías.

    Atributos:
        name (StringField): Nombre de la categoría.
    """
    name = StringField(
        max_length=120
    )


class Faculty(Document):
    """
    Modelo para representar las facultades.

    Atributos:
        name (CharField): Nombre descriptivo de la facultad.
    """
    name = StringField(max_length=255)


class Event(Document):
    """
    Modelo para representar los eventos

    Atributos:
        title (CharField): titulo descriptivo del evento.
        description (CharField): descripción del evento.
        categories (CharField): categorias del evento.
        date (CharField): fecha de realización del evento.
        location (CharField): ubicación del evento.
    """
    title = StringField(
        max_length=255
    )

    description = StringField(
        max_length=512
    )

    categories = ListField(ReferenceField
                           (Category,
                            reverse_delete_rule=NULLIFY)
                           )

    date = DateTimeField(

    )

    location_id = StringField()

    def get_location(self):
        # Realiza una consulta a la base de datos de Oracle para obtener la ubicación
        location = Location.objects.get(id=self.location_id)
        return location


class Program(Document):
    """
    Modelo para representar los programas académicos.

    Atributos:
        name (CharField): Nombre descriptivo del programa.
        facultyId (IntegerField): Identificador único de la facultad a la que pertenece.
    """
    name = StringField(
        max_length=255
    )

    facultyId = ReferenceField(
        Faculty,
        reverse_delete_rule=mongoengine.CASCADE
    )
