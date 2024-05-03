from django.contrib import admin
from .models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']  # Customize the fields to display in the admin list view
    search_fields = ['name']  # Enable searching by name
    list_filter = ['user'] 
