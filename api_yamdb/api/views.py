from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.core.mail import send_mail
from .serializers import UserRegistraionSerializer


class AuthView(APIView):

    def post(self, request):
        serializer = UserRegistraionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            send_mail(
                subject='Верификация',
                message=conf_pass,  
                from_email='test@yamdb.ru',
                recipient_list=[,],
                fail_silently=True,
            )
            return status.HTTP_200_OK
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )