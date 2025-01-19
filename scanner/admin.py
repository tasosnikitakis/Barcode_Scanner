from django.contrib import admin
from .models import Product

@admin.register(Product)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'price', 'description')  # Fields to display in the admin list view
    search_fields = ('name', 'barcode')         # Enable search functionality
