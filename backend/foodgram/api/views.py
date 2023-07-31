from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework import filters
from rest_framework.decorators import action
from django.db.models import Sum
from api.filter import RecipeFilter
from api.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

from api import permissions
from recipes.models import (Recipe, Tag, Ingredient,
                            ShoppingCart, IngredientsInRecipe, Favorite)
from api.serializers import (RecipeResponseSerializer, TagSerializer,
                             IngredientSerializer, RecipeRequestSerializer,
                             RecipeShortResponseSerializer)


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeResponseSerializer
    permission_classes = (permissions.IsAuthorOrReadOnlyPermission,)
    pagination_class = (CustomPagination)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = RecipeFilter
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD']:
            return (permissions.ReadOnlyPermission(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return RecipeRequestSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping__user=user
        ).values('ingredient__name',
                 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        shopping_cart = (
            f'Список покупок для: {user.get_full_name()}\n\n'
        )
        shopping_cart += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f' - {ingredient["amount"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            for ingredient in ingredients
        ])
        filename = f'{user.username}_shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.to_add(Favorite, request.user, pk)
        if request.method == 'DELETE':
            return self.to_delete(Favorite, request.user, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.to_add(ShoppingCart, request.user, pk)
        if request.method == 'DELETE':
            return self.to_delete(ShoppingCart, request.user, pk)

    def to_add(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortResponseSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def to_delete(self, model, user, pk):
        recipe = model.objects.filter(user=user, recipe__id=pk)
        if not recipe.exists():
            return Response({'errors': 'Рецепт уже удален'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAdminOrReadOnlyPermission,)
    pagination_class = None


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAdminOrReadOnlyPermission,)
    pagination_class = None
    search_fields = ('name',)
