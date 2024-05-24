from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class RecipeUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
    
class Recipe(models.Model):
    seller = models.ForeignKey(RecipeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)
    avg_rating = models.FloatField(default=0)
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    customer = models.ForeignKey(RecipeUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer} - {self.recipe} ({self.score})'
