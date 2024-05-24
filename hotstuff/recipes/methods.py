from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.db.models import Avg


def get_access_token(email, password):
    try:
        user = RecipeUser.objects.get(email=email)
        if password == user.password:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            return None
    except RecipeUser.DoesNotExist:
        return None
    

def login_required(function):
    def wrap(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap

def update_avg_rating(recipe):
    avg_rating = recipe.rating_set.aggregate(Avg('score'))['score__avg']
    recipe.avg_rating = avg_rating if avg_rating is not None else 0
    recipe.save()