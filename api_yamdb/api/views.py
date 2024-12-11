from rest_framework import status, viewsets, filters
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .serializers import UserRegistraionSerializer, ObtainTokenSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from users.models import CustomUser
from .utils import verification
from .permissions import AdminRole


class AuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistraionSerializer(data=request.data)
        cur_user = request.data.get('username')
        if not CustomUser.objects.filter(username=cur_user).exists():
            if serializer.is_valid():
                serializer.save()
                verification(request.data.get('username'), cur_email=request.data.get('email'))
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        verification(cur_user=request.data.get('username'), cur_email=request.data.get('email'))
        return Response(
            {request.data.get('email'): request.data.get('username')},
            status=status.HTTP_200_OK
        )


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(CustomUser, username=request.data.get('username'))
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
