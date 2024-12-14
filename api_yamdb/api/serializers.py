from django.db.models import Avg
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

class UserRegistraionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Невозможное имя пользователя'
            )
        if CustomUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        if not CustomUser.objects.filter(username=data
                                         .get('username')).exists():
            return Response(
                'Такого пользователя не существует',
                status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(username=data.get('username'))
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError("Неверный код подтверждения.")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class CategorySerializer(serializers.ModelSerializer):
    ''' Сериализатор для категорий.'''

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    ''' Сериализатор для жанров.'''

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class TitleEditSerializer(serializers.ModelSerializer):
    """Сериализатор для записи и изменения произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, score):
        if not 0 < score <= 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return score

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = data.get('title')
            author = self.context['request'].user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.')
        return data

class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('author', 'id', 'text', 'pub_date', 'review')
        model = Comment
