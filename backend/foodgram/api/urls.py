from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('recipes', views.RecipeViewset, basename='recipes')
router.register('tags', views.TagViewset)
router.register('ingredients', views.IngredientViewset)


urlpatterns = [
    path('', include(router.urls)),
]
