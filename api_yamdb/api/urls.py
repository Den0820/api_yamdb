from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import 

router = DefaultRouter()
#router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
]
