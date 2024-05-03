from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers.ingredient_serializer import IngredientSerializer

from django.contrib.auth.decorators import permission_required
from openai import OpenAI
import requests
import json
import os



class IngredientView(APIView):
  permission_classes = (IsAuthenticated, )

  def get(self, request):
    try:
      ingredients = ingredients.objects.all()
      serializer = IngredientSerializer(ingredients, many=True)
      return Response(serializer.data)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  def post(self, request):
    serializer = CreateIngredientSerializer(data=request.data)
    if serializer.is_valid():
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientDetailView(APIView):
  permission_classes = (IsAuthenticated, )

  def delete(self, request, pk):
    try:
      ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
      
    ingredient.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class GenerateRecipeView(APIView):
  permission_classes = (AllowAny, )

  def get_video(self, query):
    access_key = "AIzaSyCFCuHNxq55lcdAzJXvOoVEKsGLrjVNySE"

    if not query:
      return JsonResponse({'error': 'Missing search query parameter'}, status=400)

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}recipe&key={access_key}"
    
    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()
      return data

    else:
      return JsonResponse({'error': 'Youtube API request failed'}, status=response.status_code)

  
  def get(self, request, *args, **kwargs):
    pass

  # @permission_required('recipes.general_user')
  def post(self, request, *args, **kwargs):
    client = OpenAI()
    ingredients = request.data.get('ingredients')

    try:
      completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a recipe expert. Given any list of ingredients, you are able suggest delicious food recipes."},
        {"role": "user", "content": f"Using the following ingredients: {ingredients}; provide a list of 5 recipes of different types that I can make at home. Provide detailed instructions, name of recipe, ingredients, and a image link of recipe in JSON format"}
      ]
      )
      
      recipe_data = completion.choices[0].message.content      
      print(recipe_data)
      
      # MOCK RESPONSE FROM OPENAPI
    # recipe_data= '{\n    "recipes": [\n        {\n            "name": "Strawberry French Toast",\n            "ingredients": ["Brioche Bread", "Eggs", "Strawberries", "Sugar"],\n            "instructions": "1. Slice the brioche bread into thick slices. 2. In a bowl, whisk together eggs and sugar. 3. Dip each bread slice into the egg mixture. 4. Cook the bread slices on a griddle until golden brown. 5. Top with fresh strawberries and serve.",\n            "image": "https://www.example.com/strawberry_french_toast.jpg"\n        },\n        {\n            "name": "Strawberry Shortcake",\n            "ingredients": ["Flour", "Strawberries", "Sugar"],\n            "instructions": "1. Prepare shortcake by mixing flour, sugar, and butter until crumbly. 2. Bake the shortcake until golden brown. 3. Cut strawberries and mix with sugar. 4. Slice the shortcake, layer with strawberries, and top with whipped cream.",\n            "image": "https://www.example.com/strawberry_shortcake.jpg"\n        },\n        {\n            "name": "Strawberry Pancakes",\n            "ingredients": ["Flour", "Eggs", "Strawberries", "Sugar"],\n            "instructions": "1. Mix flour, eggs, sugar, and diced strawberries to make pancake batter. 2. Cook the pancakes on a griddle until golden brown. 3. Serve with sliced strawberries and maple syrup.",\n            "image": "https://www.example.com/strawberry_pancakes.jpg"\n        },\n        {\n            "name": "Strawberry Muffins",\n            "ingredients": ["Flour", "Eggs", "Strawberries", "Sugar"],\n            "instructions": "1. Mix flour, eggs, sugar, and diced strawberries to make muffin batter. 2. Pour the batter into muffin tins. 3. Bake the muffins until golden and fully cooked. 4. Enjoy the strawberry muffins warm or at room temperature.",\n            "image": "https://www.example.com/strawberry_muffins.jpg"\n        },\n        {\n            "name": "Strawberry Tarts",\n            "ingredients": ["Flour", "Eggs", "Strawberries", "Sugar"],\n            "instructions": "1. Prepare tart crust with flour, sugar, and butter. 2. Fill the crust with sliced strawberries. 3. Bake the tarts until the crust is golden and the strawberries are juicy. 4. Serve the strawberry tarts with a dollop of whipped cream.",\n            "image": "https://www.example.com/strawberry_tarts.jpg"\n        }\n    ]\n}'
      recipe_data = json.loads(recipe_data)
    # print(type(recipe_data), recipe_data)

      # Add images -> FUTURE FEATURE  
      for recipe in recipe_data["recipes"]:

        recipe["video"] = self.get_video(recipe.get("name"))

      json.dumps(recipe_data)

      return JsonResponse(recipe_data, safe=False)
    except Exception as e:
      print(f"OpenAI API Error: {e}")
  
  