from django.contrib import admin
from .models import (
    Company, Contact, Department, ContactDepartment, Interaction, 
    Opportunity, OpportunityStage, OpportunityStageHistory, 
    ProductService, OpportunityProductService, Role, 
    UserAccount, UserRole, Contract, Category, 
    DeliveryCertificate, Equipment
)

# Registramos los modelos en el admin
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nit', 'name', 'industry', 'email', 'phone', 'country')
    search_fields = ('nit', 'name', 'industry')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'first_name', 'last_name', 'email', 'phone', 'company')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('company',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'description')
    search_fields = ('department_name',)

@admin.register(ContactDepartment)
class ContactDepartmentAdmin(admin.ModelAdmin):
    list_display = ('contact', 'department', 'assignment_date')
    list_filter = ('department', 'assignment_date')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('interaction_id', 'contact', 'interaction_date', 'interaction_type')
    list_filter = ('interaction_type', 'interaction_date')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('opportunity_id', 'opportunity_name', 'company', 'status', 'creation_date')
    search_fields = ('opportunity_name',)
    list_filter = ('status', 'creation_date')

@admin.register(OpportunityStage)
class OpportunityStageAdmin(admin.ModelAdmin):
    list_display = ('stage_id', 'stage_name', 'description')

@admin.register(OpportunityStageHistory)
class OpportunityStageHistoryAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'stage', 'change_date')

@admin.register(ProductService)
class ProductServiceAdmin(admin.ModelAdmin):
    list_display = ('product_service_id', 'product_service_name', 'price', 'description')

@admin.register(OpportunityProductService)
class OpportunityProductServiceAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'product_service', 'quantity', 'negotiated_price')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'description')

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'created_at', 'last_login')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'start_date', 'end_date', 'monthly_value', 'company')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'description')

@admin.register(DeliveryCertificate)
class DeliveryCertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'contract', 'user', 'delivery_date')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_id', 'inventory_code', 'description', 'active', 'available_quantity', 'category')
    search_fields = ('inventory_code', 'description')
    list_filter = ('active', 'category')
