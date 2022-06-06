from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from reviews.models import (
    Category, Comment, Genre, Review, Title
)

from .filters import TitleFilter
from .permissions import AdminPermission
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer
)
from .viewsets import CreateRetrieveListViewSet


class CategoryViewSet(CreateRetrieveListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    # permission_classes = (AdminPermission,)


@api_view(['DELETE'])
# @permission_classes([AdminPermission])
def category_delete(request, slug):
    if Category.objects.filter(slug=slug).exists():
        Category.objects.filter(slug=slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class GenreViewSet(CreateRetrieveListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    # permission_classes = (AdminPermission,)


@api_view(['DELETE'])
# @permission_classes([AdminPermission])
def genre_delete(request, slug):
    if Genre.objects.filter(slug=slug).exists():
        Genre.objects.filter(slug=slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (AdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category_slug = self.request.data.get('category')
        if Category.objects.filter(slug=category_slug).exists():
            category = Category.objects.get(slug=category_slug)
        else:
            raise serializers.ValidationError(
                'Введите существующую категорию!'
            )
        genre_slugs = self.request.data.get('genre')
        genre = []
        for genre_slug in genre_slugs:
            if Genre.objects.filter(slug=genre_slug).exists():
                genre.append(Genre.objects.get(slug=genre_slug))
            else:
                raise serializers.ValidationError('Введите существующий жанр!')
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        category_slug = self.request.data.get('category')
        if Category.objects.filter(slug=category_slug).exists():
            category = Category.objects.get(slug=category_slug)
        else:
            raise serializers.ValidationError(
                'Введите существующую категорию!'
            )
        genre_slugs = self.request.data.get('genre')
        genre = []
        for genre_slug in genre_slugs:
            if Genre.objects.filter(slug=genre_slug).exists():
                genre.append(Genre.objects.get(slug=genre_slug))
            else:
                raise serializers.ValidationError('Введите существующий жанр!')
        serializer.save(category=category, genre=genre)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    # permission_classes = настроить для разных запросов

    def get_queryset(self):
        pk = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=pk)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        pk = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=pk)
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение!'
            )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    # permission_classes = настроить для разных запросов

    def get_queryset(self):
        pk = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=pk)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        pk = self.kwargs.get("title_id")
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=pk)
        )
