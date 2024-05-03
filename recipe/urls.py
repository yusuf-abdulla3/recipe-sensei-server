from django.urls import path
from . import views

urlpatterns = [
  path('ingredients', views.IngredientView.as_view(), name='ingredient'),
  path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),

  path('generate', views.GenerateRecipeView.as_view(), name='generate_recipe'),

]