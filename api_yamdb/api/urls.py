from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

all_api_urls = [
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(all_api_urls)),
]
