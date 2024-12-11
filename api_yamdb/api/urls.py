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
router_v1.register('users', UserViewSet)
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
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

all_api_urls = [
    path('', include(router_v1.urls)),
]

user_urls = [
    path('signup/', AuthView.as_view()),
    path('token/', ObtainTokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(all_api_urls)),
    path('v1/auth/', include(user_urls)),
]
