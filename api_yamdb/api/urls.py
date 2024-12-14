from django.urls import include, path
from rest_framework import routers

from api.views import (
    AuthView,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ObtainTokenView,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', AuthView.as_view()),
    path('v1/auth/token/', ObtainTokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]
