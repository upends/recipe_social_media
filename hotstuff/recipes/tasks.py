from celery import shared_task
from datetime import datetime
from .models import Recipe

@shared_task
def my_periodic_task():
    print("Resizing Image")
  
    
    recipes_to_resize = Recipe.objects.filter(image_resized=False)

    for recipe in recipes_to_resize:
        print(recipe)
        recipe.resize_image(1)

    print("Image Resized")