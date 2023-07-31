from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('recipes', views.RecipeViewset)
router.register('tags', views.TagViewset)
router.register('ingredients', views.IngredientViewset)


urlpatterns = [
    path('', include(router.urls)),
]
