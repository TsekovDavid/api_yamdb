from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import (Category, Comment, Genre, Review, Title, User)
from .filters import TitleFilter
from .permissions import IsAdmin#AdminPermission
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, SignupSerializer, TitleSerializer, TokenSerializer, UserSerializer
)
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
    permission_classes = (AdminPermission,)
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
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=pk)
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def code(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        email = serializer.data['email']
        user = get_object_or_404(User, username=username, email=email)
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения'
    message = f'{confirmation_code} - Используйте для авторизации на сайте'
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
