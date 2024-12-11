from django.urls import include, path
from rest_framework import routers
from api.views import CategoryViewSet, CommentViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, AuthView, ObtainTokenView, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)
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

urlpatterns = [
    path('v1/', include(all_api_urls)),
    path('v1/auth/signup/', AuthView.as_view()),
    path('v1/auth/token/', ObtainTokenView.as_view()),
]
