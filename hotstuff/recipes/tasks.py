from celery import shared_task
from datetime import datetime
from .models import Recipe, RecipeUser
import pandas as pd
import os
from django.core.mail import EmailMessage

@shared_task
def image_resize_task():
    print("Resizing Image")
  
    
    recipes_to_resize = Recipe.objects.filter(image_resized=False)

    for recipe in recipes_to_resize:
        print(recipe)
        recipe.resize_image(1)

    print("Image Resized")

@shared_task
def server_status():
    print("Sending server status mail")
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS')
    if EMAIL_RECIPIENTS:
        EMAIL_RECIPIENTS = EMAIL_RECIPIENTS.split(',')
    else:
        EMAIL_RECIPIENTS = []
    EMAIL_SENDER  =os.getenv('EMAIL_HOST_USER')
    email = EmailMessage(
        'Server update',
        'Server is running fine',
        EMAIL_SENDER, 
        EMAIL_RECIPIENTS,  
    )
    email.send()

@shared_task
def export_users_to_csv():
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"user_data_{today_date}.csv"
    file_path = os.path.join('media', file_name)
    users = RecipeUser.objects.all()
    
    # Create a DataFrame to hold the data
    data = {
        'Username': [user.username for user in users],
        'Email': [user.email for user in users],
        'Is Customer': [user.is_customer for user in users],
        'Is Seller': [user.is_seller for user in users]
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)