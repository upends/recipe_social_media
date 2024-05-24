from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .serializers import RecipeUserSerializer, RecipeSerializer, RatingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import RecipeUser, Recipe
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .methods import *
from django.contrib import messages


def home(request):
    return redirect("recipe")

@api_view(['POST'])
def seller_registration_view(request):
    if request.method == 'POST':
        serializer = RecipeUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_seller=True)
            return Response({'message': 'Seller created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def customer_registration_view(request):
    if request.method == 'POST':
        serializer = RecipeUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_customer=True)
            return Response({'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token_obtain_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = RecipeUser.objects.get(email=email)
        if password != user.password:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_recipe(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recipe(request, id):
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_recipe(request):
    user = request.user
    if not user.is_seller:
        return Response({"detail": "User is not a seller."}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()  
    serializer = RecipeSerializer(data=data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save(seller=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('id')
    return render(request, 'recipe_list.html', {'recipes': recipes})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_recipe(request, recipe_id):
    user = request.user
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        return Response({"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

    if user != recipe.seller:
        return Response({"detail": "You are not allowed to update this recipe."}, status=status.HTTP_403_FORBIDDEN)

    serializer = RecipeSerializer(recipe, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rating(request, recipe_id):
    user = request.user
    
    if not user.is_customer:
        return Response({"detail": "User is not a customer."}, status=status.HTTP_403_FORBIDDEN)

    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        return Response({"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['customer'] = user.id
    data['recipe'] = recipe_id
    
    serializer = RatingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        update_avg_rating(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        tokens = get_access_token(email, password)
        if tokens:
            access_token = tokens['access']
            # Store the access token in a cookie
            response = redirect('recipe_list')  
            response.set_cookie('access_token', access_token)
            return response
        else:
            return HttpResponse("Login failed")
    else:
        return render(request, 'login.html')


def registration_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_seller = request.POST.get('is_seller')
    
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            }
        serializer = RecipeUserSerializer(data=data)
        
        if is_seller:
            if serializer.is_valid():
                serializer.save(is_seller=True)
        else:
            if serializer.is_valid():
                serializer.save(is_customer=True)
       
        tokens = get_access_token(email, password)

        if tokens:
            access_token = tokens['access']
            # Store the access token in a cookie
            response = redirect('recipe_list')  
            response.set_cookie('access_token', access_token)
            return response
        else:
            return HttpResponse("Registration failed")
    return render(request, 'registration.html')


def logout_view(request):
    response = redirect('login')  
    response.delete_cookie('access_token') 
    return response


def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        score = request.POST.get('rating')

        if score:
            try:
                score = int(score)
                if 1 <= score <= 10:
                    rating = Rating()
                    rating.recipe = recipe
                    rating.customer = request.user
                    rating.score = score
                    rating.save()
                    update_avg_rating(recipe)
                    messages.success(request, f'Rating for {recipe.name} saved successfully!')
                else:
                    messages.error(request, 'Rating must be between 1 and 10.')
            except ValueError:
                messages.error(request, 'Invalid rating value.')
        else:
            messages.error(request, 'Rating is required.')

    return redirect('recipe_list')





