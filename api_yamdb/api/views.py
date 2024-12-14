from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError, MethodNotAllowed
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import AdminRole, IsAdminOrReadOnly, IsOwnerOrReadOnlyReview
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ObtainTokenSerializer,
    ReviewSerializer,
    TitleEditSerializer,
    TitleReadSerializer,
    UserRegistraionSerializer,
    UserSerializer)
from api.utils import verification
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title)
from users.models import CustomUser


class ListCreateViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    ''' Родительский вьюсет для просмотра списка,
        создания, удаления объекта.'''


class AuthView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistraionSerializer(data=request.data)
        cur_user = request.data.get('username')
        if not CustomUser.objects.filter(username=cur_user).exists():
            if serializer.is_valid():
                serializer.save()
                verification(request.data.get('username'),
                             cur_email=request.data.get('email'))
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        verification(cur_user=request.data.get('username'),
                     cur_email=request.data.get('email'))
        return Response(
            {request.data.get('email'): request.data.get('username')},
            status=status.HTTP_200_OK
        )


class ObtainTokenView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(CustomUser,
                                     username=request.data.get('username'))
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = [AdminRole]


class CategoryViewSet(ListCreateViewSet):
    ''' Вьюсет для просмотра категорий.'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'


class GenreViewSet(ListCreateViewSet):
    ''' Вьюсет для просмотра жанров.'''

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    ''' Вьюсет для работы с произведениями.'''

    queryset = Title.objects.all().order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnlyReview,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title, author=self.request.user).exists():
            raise ValidationError(detail='Может существовать только один отзыв!')
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnlyReview,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

