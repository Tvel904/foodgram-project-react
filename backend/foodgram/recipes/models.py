from django.db import models
from users.models import User

MAX_LENGTH = 200
COLOR_MAX_LENGTH = 7


class Tag(models.Model):
    name = models.CharField(
        'Название тэга', max_length=MAX_LENGTH, unique=True)
    color = models.CharField(
        'Цвет тэга', max_length=COLOR_MAX_LENGTH,
        default="#ffffff", unique=True)
    slug = models.SlugField(
        'Слаг тэга', max_length=MAX_LENGTH, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента', max_length=MAX_LENGTH)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=MAX_LENGTH)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта')
    name = models.CharField('Название', max_length=MAX_LENGTH)
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Текстовое описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах')
    tags = models.ManyToManyField(
        Tag, related_name='recipe', verbose_name='Тэг')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipe', through='IngredientsInRecipe',
        verbose_name='Ингредиенты')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='in_recipe',
        verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='which_ingredients',
        verbose_name='Рецепт')
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount} '
        )


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping', verbose_name='Рецепт')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Рецепт')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} в избранных у {self.user}'
