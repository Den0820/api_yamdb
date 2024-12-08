from rest_framework import serializers
from reviews.models import Review, Comment
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='user',
        read_only=True
    )
    score_avg = serializers.SerializerMethodField()

    def get_score_avg(self, obj):
        return obj.title.reviews.aggregate(Avg('score'))['score__avg']

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть по 10-бальной шкале!'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST' and Review.objects.filter(
            title=request.parser_context['kwargs']['title_id'],
            author=request.user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review



class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='user',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
