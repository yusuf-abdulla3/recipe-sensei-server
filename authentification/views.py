from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers.register_serializer import RegisterSerializer


class HomeView(APIView):

  permission_classes = (IsAuthenticated, )

  def get(self, request):
    content = {'message': 'Welcome to the JWT Authentication page using React Js and Django'}

    return Response(content)

class LogoutView(APIView):
  permission_classes = (IsAuthenticated, )
  
  def post(self, request):
    try:
      refresh_token = request.data["refresh_token"]
      token = RefreshToken(refresh_token)
      token.blacklist()
      return HttpResponse(status=205)
    except Exception as e:
      print(e)
      return HttpResponse(status=400)

class RegisterView(APIView):
  queryset=User.objects.all()

  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


