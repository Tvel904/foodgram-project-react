from django.contrib import admin
from recipes.models import (Recipe, Tag, ShoppingCart,
                            Ingredient, IngredientsInRecipe, Favorite)
from users.models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name')


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientsInRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'followers')
    list_filter = ('author', 'name', 'tags')
    inlines = [
        IngredientInRecipeInline,
    ]

    def followers(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(IngredientsInRecipe)
admin.site.register(Subscribe)
