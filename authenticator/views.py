from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user
from rest_framework.authtoken.models import Token
from authenticator.models import VUser
from rest_framework import status
user = get_user
class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = VUser.objects.create_user(
                username=username,
                password=password,
            )
            token, _ = Token.objects.get_or_create(user=user)
        except Exception as e:
            return Response({"error": True, 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "id": user.id,
            "token": token.key,
            "username":user.username
        }, status=status.HTTP_200_OK)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)


            return Response(
                {
                    "token": token.key,
                    "username": user.username,
                    "id": user.id
                },
                status=status.HTTP_200_OK
            )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



