# serializers.py

from rest_framework import serializers
from .models import RecipeUser, Recipe, Rating

class RecipeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeUser
        fields = ['username', 'email', 'password', 'is_customer', 'is_seller']
        extra_kwargs = {'password': {'write_only': True}} 


class RecipeSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ['id', 'seller', 'name', 'description', 'image', 'created_at', 'updated_at', 'avg_rating']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['customer', 'recipe', 'score', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 