from rest_framework import serializers
from django.contrib.auth.models import User
from recipe.models import Ingredient

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class IngredientSerializer(serializers.ModelSerializer):
  username = UserSerializer(read_only=True)
  name = serializers.CharField(required=True)

  class Meta:
    model = Ingredient
    fields=(
      'id'
      'username', 
      'name'
    )


class CreateIngredientSerializer(serializers.ModelSerializer):
  name = serializers.CharField(required=True)

  class Meta:
    model = Ingredient
    fields=(
      'user', 
      'name'
    )  

  def create(self, validated_data):
    try: 
      user = User.objects.get(username=validated_data["username"])
    except Exception as e:
      raise serializers.ValidationError({"ingredient_serializer_line_20": "Invalid User."})

    ingredient = Ingredient.objects.create(
      user=user,
      name=validated_data["name"],
    )

    ingredient.save()
    return ingredient

