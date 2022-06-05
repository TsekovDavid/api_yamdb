from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, category_delete, GenreViewSet, genre_delete,
    ReviewViewSet, TitleViewSet
)


router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/categories/<slug:slug>/',
        category_delete,
        name='category_delete'
    ),
    path(
        'v1/genres/<slug:slug>/',
        genre_delete,
        name='genre_delete'
    ),
]
