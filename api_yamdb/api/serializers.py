from django.core import validators
from rest_framework import serializers, status
from rest_framework.response import Response

from api_yamdb.settings import (
    EMAIL_ML,
    USERNAME_ML,
    USERNAME_REGEX
)
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
            raise serializers.ValidationError('Неверный код подтверждения.')
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_ML,
        validators=(validators.MaxLengthValidator(EMAIL_ML),)
    )
    username = serializers.SlugField(
        max_length=USERNAME_ML,
        validators=(
            validators.MaxLengthValidator(USERNAME_ML),
            validators.RegexValidator(USERNAME_REGEX)
        )
    )

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs.get('email')).exists():
            user = CustomUser.objects.get(email=attrs.get('email'))
            if user.username != attrs.get('username'):
                raise serializers.ValidationError(
                    {
                        'error': 'Email is already used!'
                    }
                )
        elif CustomUser.objects.filter(
                username=attrs.get('username')).exists():
            user = CustomUser.objects.get(username=attrs.get('username'))
            if user.email != attrs.get('email'):
                raise serializers.ValidationError(
                    {
                        'error': 'Username is already used!'
                    }
                )
        return super().validate(attrs)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                {
                    'error': 'You cannot use "me" as username!'
                }
            )
        return value

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )
        lookup_field = 'username'
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

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
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
        error_messages={'min_value': 'Оценка должна быть больше 0!',
                        'max_value': 'Оценка должна быть не больше 10!'}
    )

    class Meta:
        fields = '__all__'
        model = Review

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


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
