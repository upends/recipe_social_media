from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RecipeUser, Recipe, Rating
from django.contrib.auth.admin import UserAdmin


class RecipeUserAdmin(UserAdmin):
    list_display = ('email', 'is_customer', 'is_seller', 'is_staff', 'is_active')
    list_filter = ('is_customer', 'is_seller', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_customer', 'is_seller', 'is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_customer', 'is_seller', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(RecipeUser, RecipeUserAdmin)
admin.site.register(Recipe)
admin.site.register(Rating)
