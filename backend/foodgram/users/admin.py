from django.contrib import admin
from recipes.models import (Recipe, Tag, ShoppingCart,
                            Ingredient, IngredientsInRecipe, Favorite)
from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'followers')
    list_filter = ('author', 'name', 'tags')

    def followers(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(IngredientsInRecipe)
admin.site.register(Subscribe)
