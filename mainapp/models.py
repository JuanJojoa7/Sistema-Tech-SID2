from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

"""------------------------ PostgreSQL Models -------------------------------------------"""

class ProductService(models.Model):
    product_service_id = models.CharField(max_length=20, primary_key=True)
    product_service_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

class OpportunityStage(models.Model):
    stage_id = models.CharField(max_length=20, primary_key=True)
    stage_name = models.CharField(max_length=50)
    description = models.TextField()

class Company(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=60)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    creation_date = models.DateField()

class Contact(models.Model):
    contact_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    last_interaction_date = models.DateField()

class Interaction(models.Model):
    interaction_id = models.CharField(max_length=20, primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    interaction_date = models.DateField()
    interaction_type = models.CharField(max_length=50)
    notes = models.TextField()

class Opportunity(models.Model):
    opportunity_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    opportunity_name = models.CharField(max_length=100)
    description = models.TextField()
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2)
    estimated_date = models.DateField()
    estimated_close_date = models.DateField()
    status = models.CharField(max_length=20)
    success_probability = models.DecimalField(max_digits=6, decimal_places=2)

class OpportunityProductService(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    product_service = models.ForeignKey(ProductService, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    negotiated_price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = (('opportunity', 'product_service'),)

class OpportunityStageHistory(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    stage = models.ForeignKey(OpportunityStage, on_delete=models.CASCADE)
    change_date = models.DateField()
    notes = models.TextField()

    class Meta:
        unique_together = (('opportunity', 'stage', 'change_date'),)

class Department(models.Model):
    department_id = models.CharField(max_length=20, primary_key=True)
    department_name = models.CharField(max_length=50)
    description = models.TextField()

class ContactDepartment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assignment_date = models.DateField()

    class Meta:
        unique_together = (('contact', 'department'),)

class Contract(models.Model):
    contract_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_value = models.DecimalField(max_digits=15, decimal_places=2)

class DeliveryCertificate(models.Model):
    certificate_id = models.CharField(max_length=20, primary_key=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    notes = models.TextField()

class SQLInventoryEquipment(models.Model):  # Renamed to avoid conflict with MongoDB model
    equipment_id = models.CharField(max_length=20, primary_key=True)
    certificate = models.ForeignKey(DeliveryCertificate, on_delete=models.CASCADE)
    inventory_code = models.CharField(max_length=20, unique=True)
    equipment_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField()
    active = models.BooleanField()

class SQLCategory(models.Model):  # Renamed to avoid conflict with MongoDB model
    category_id = models.CharField(max_length=20, primary_key=True)
    category_name = models.CharField(max_length=50)

class UserAccount(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    last_login = models.DateTimeField()

class Role(models.Model):
    role_id = models.CharField(max_length=20, primary_key=True)
    role_name = models.CharField(max_length=50)
    description = models.TextField()

class UserRole(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'role'),)


"""--------------------- MongoDB Models -------------------------------------------"""

class MongoCategory(Document):
    category_id = fields.StringField(required=True, unique=True, max_length=20)
    category_name = fields.StringField(required=True, max_length=50)
    description = fields.StringField()  # Additional details for the category

    meta = {'collection': 'categories'}


class EquipmentSpecifications(EmbeddedDocument):
    spec_key = fields.StringField(required=True)  # Specification name, e.g., "RAM"
    spec_value = fields.StringField(required=True)  # Specification value, e.g., "16GB"


class MongoEquipment(Document):
    equipment_id = fields.StringField(required=True, unique=True, max_length=20)
    category = fields.ReferenceField(MongoCategory, required=True)  # Relationship with category
    name = fields.StringField(required=True, max_length=100)
    brand = fields.StringField(max_length=50)
    model = fields.StringField(max_length=50)
    description = fields.StringField()  # General description
    price = fields.DecimalField(required=True, precision=2)
    stock_quantity = fields.IntField(required=True)
    warranty_period = fields.StringField()  # Warranty period
    release_date = fields.DateField()  # Release date
    active = fields.BooleanField(default=True)
    specifications = fields.EmbeddedDocumentListField(EquipmentSpecifications)  # List of specifications
    image_url = fields.URLField()  # Image URL

    meta = {'collection': 'equipments'}


class RentalRequest(Document):
    request_id = fields.StringField(required=True, unique=True, max_length=20)
    user_id = fields.StringField(required=True, max_length=20)  # ID of the customer making the request
    equipment = fields.ReferenceField(MongoEquipment, required=True)  # Requested equipment
    request_date = fields.DateTimeField(required=True)
    status = fields.StringField(choices=['pending', 'approved', 'rejected'], default='pending')  # Request status

    meta = {'collection': 'rental_requests'}


class ActiveRental(Document):
    rental_id = fields.StringField(required=True, unique=True, max_length=20)
    contract_id = fields.StringField(required=True, max_length=20)  # Contract ID
    equipment = fields.ReferenceField(MongoEquipment, required=True)  # Rented equipment
    start_date = fields.DateField(required=True)
    end_date = fields.DateField()

    meta = {'collection': 'active_rentals'}


class MongoContract(Document):
    contract_id = fields.StringField(required=True, unique=True, max_length=20)
    customer_id = fields.StringField(required=True, max_length=20)  # Customer ID in CRM
    start_date = fields.DateField(required=True)
    end_date = fields.DateField()
    monthly_value = fields.DecimalField(required=True, precision=2)
    delivery_certificates = fields.ListField(fields.StringField())  # Related delivery certificate IDs
    active_rentals = fields.ListField(fields.ReferenceField(ActiveRental))  # Related active rentals

    meta = {'collection': 'contracts'}
