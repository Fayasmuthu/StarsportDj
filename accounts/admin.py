# Register your models here.
from django.contrib import admin
from .models import CustomerAddress


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'full_name','address_type')
    list_filter = ('customer',)
    search_fields = ('customer__username',)
    ordering = ('customer', 'is_default')

    readonly_fields = ['customer']
