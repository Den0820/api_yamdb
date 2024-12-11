from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AuthView, ObtainTokenView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', AuthView.as_view()),
    path('v1/auth/token/', ObtainTokenView.as_view()),
]
