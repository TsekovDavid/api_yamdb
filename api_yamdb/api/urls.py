from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    genre_delete, ReviewViewSet, TitleViewSet, UserViewSet, category_delete, code, signup, token
)


app_name = 'api'
v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='login'),
    path('v1/auth/code/', code, name='code'),
    path('v1/categories/<slug:slug>/', category_delete, name='category_delete'),
    path('v1/genres/<slug:slug>/', genre_delete, name='genre_delete'),
]
