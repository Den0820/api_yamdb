from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound, ValidationError, PermissionDenied)
from django.db.models import Avg
from reviews.models import Review, Comment, Title
from .serializers import ReviewSerializer, CommentSerializer


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
