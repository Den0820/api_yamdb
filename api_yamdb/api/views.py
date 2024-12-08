from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import (
    NotFound, 
    PermissionDenied,
    ValidationError)
from rest_framework.response import Response


from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer)
from reviews.models import (
    Category, 
    Comment, 
    Genre, 
    Review, 
    Title)


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Получение списка всех отзывов для произведения."""
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        """Добавление нового отзыва."""
        title_id = self.kwargs.get('title_id')
        if not Title.objects.filter(id=title_id).exists():
            raise NotFound('Произведение не найдено.')
        if Review.objects.filter(
                title_id=title_id, author=self.request.user
        ).exists():
            raise ValidationError('Вы уже оставили отзыв на это произведение.')
        serializer.save(title_id=title_id, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Получение списка всех комментариев к отзыву."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return Comment.objects.select_related('review').filter(
            review_id=review_id, review__title_id=title_id
        )

    def perform_create(self, serializer):
        """Добавление комментария к отзыву."""
        serializer.save(
            review=Review.objects.filter(
                id=self.kwargs.get('review_id'),
                title_id=self.kwargs.get('title_id')
            ).first(),
            author=self.request.user
        )

