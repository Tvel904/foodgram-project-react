import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.rest_framework.FilterSet):
    tags = django_filters.CharFilter(field_name='slug',
                                     method='filter_tags', distinct=True)
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited', method='filter_is_favorited')

    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart'
    )

    author = django_filters.NumberFilter(
        field_name='author', method='filter_author'
    )

    def filter_tags(self, queryset, name, value):
        request_value = self.request.GET.getlist('tags')
        return queryset.filter(tags__slug__in=request_value)

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(shopping__user=self.request.user)

    def filter_author(self, queryset, name, value):
        request_value = self.request.GET.get('author')
        return queryset.filter(author__id__in=request_value)

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')
