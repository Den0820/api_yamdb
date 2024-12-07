from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    ''' Вьюсет для просмотра категорий.'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.ModelViewSet):
    ''' Вьюсет для просмотра жанров.'''

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)


class TitleViewSet(viewsets.ModelViewSet):
    ''' Вьюсет для просмотра произведений.'''

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
