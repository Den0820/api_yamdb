from rest_framework import serializers
from reviews.models import Review, Comment
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'title',
            'author',
            'text',
            'score',
            'pub_date',
            'average_rating'
        ]
        read_only_fields = ['title']

    def get_average_rating(self, obj):
        """Вычисление среднего рейтинга для произведения."""
        title_id = obj.title.id
        average_rating = Review.objects.filter(title_id=title_id).aggregate(
            Avg('score')
        )['score__avg']
        return round(average_rating, 1) if average_rating is not None else 0


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'review', 'author', 'text', 'pub_date']
        read_only_fields = ['review']
