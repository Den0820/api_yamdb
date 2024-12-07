from rest_framework import serializers
from reviews.models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']

        read_only_fields = ['title']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'author', 'text', 'pub_date']

        read_only_fields = ['review']
