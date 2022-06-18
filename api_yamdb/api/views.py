import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import IsAdmin, IsAuthorOrModeratorOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)
from .viewsets import CreateDestroyListViewSet


class CategoryGenreViewSet(CreateDestroyListViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdmin | ReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateUpdateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly,)

    @property
    def title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrModeratorOrReadOnly,
                          IsAuthenticatedOrReadOnly,)

    @property
    def review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review
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
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer)
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if user.confirmation_code != confirmation_code:
        return Response(
            'Код подтверждения неверный', status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    token_data = {'token': str(refresh.access_token)}
    return Response(token_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    try:
        user, created = User.objects.get_or_create(
            **serializer.validated_data,
            confirmation_code=confirmation_code
        )
    except Exception as error:
        return Response(
            f'Произошла ошибка ->{error}<-',
            status=status.HTTP_400_BAD_REQUEST
        )
    send_mail(
        subject='Код подтверждения',
        message=f'{user.confirmation_code} - Код для авторизации на сайте',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email])
    return Response(serializer.data, status=status.HTTP_200_OK)
