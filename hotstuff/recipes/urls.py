from django.urls import path
from . import views

urlpatterns = [
    path('api/sellers/register/', views.seller_registration_view, name='seller-register'),
    path('api/customers/register/', views.customer_registration_view, name='customer-register'),
    path('api/token/', views.token_obtain_view, name='token-obtain'),
    path('api/get_all_recipe', views.get_all_recipe, name='get_all_recipe'),
    path('api/get_recipe/<int:id>', views.get_recipe, name='get_recipe'),
    path('api/recipe/create', views.create_recipe, name='create_recipe'),
    path('api/recipe/<int:recipe_id>/update', views.update_recipe, name='update_recipe'),
    path('api/recipe/<int:recipe_id>/give_rating', views.create_rating, name='give_rating'),
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    path('rate_recipe/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),
]
