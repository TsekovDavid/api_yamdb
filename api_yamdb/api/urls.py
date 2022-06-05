from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, category_delete, GenreViewSet, genre_delete, TitleViewSet
)


router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'categories/<slug:slug>/',
        category_delete,
        name='category_delete'
    ),
    path(
        'genres/<slug:slug>/',
        genre_delete,
        name='genre_delete'
    ),
]
