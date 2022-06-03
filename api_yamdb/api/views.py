from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from reviews.models import Category, Genre, Title

from .permissions import AdminPermission
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import CreateRetrieveListViewSet


class CategoryViewSet(CreateRetrieveListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminPermission,)


@api_view(['DELETE'])
@permission_classes([AdminPermission])
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
    permission_classes = (AdminPermission,)


@api_view(['DELETE'])
@permission_classes([AdminPermission])
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre',)
