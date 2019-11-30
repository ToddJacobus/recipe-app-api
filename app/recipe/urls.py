from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# register the view with a name
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

# assign an app_name so the 'reverse' function can find it.
app_name = 'recipe'

urlpatterns = [
    # this includes all default urls, even if we create and register
    # new viewsets
    path('', include(router.urls))
]
