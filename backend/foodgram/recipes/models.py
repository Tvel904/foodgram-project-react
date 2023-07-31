from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, default="#ffffff", unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта')
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Текстовое описание')
    cooking_time = models.IntegerField(
        'Время приготовления в минутах')
    tags = models.ManyToManyField(
        Tag, related_name='recipe', verbose_name='Тэг')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipe', through='IngredientsInRecipe')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='in_recipe')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='which_ingredients')
    amount = models.IntegerField('Количество')

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount} '
        )


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping')

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.recipe} в избранных у {self.user}'
