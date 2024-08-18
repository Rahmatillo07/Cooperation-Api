from django.contrib.sites import requests
from django.shortcuts import render, redirect
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User, Chat
from .serializers import UserSerializer, ChatSerializer, RegisterSerializer, LocationUpdateSerializer
from .permissions import UserPermission, ChatPermission


class UserApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


class ChatApiView(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, ChatPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user) | Chat.objects.filter(to_user=user)

    def perform_create(self, serializer):
        serializer.save(status='pending')


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request):
        return Response({'message': "Ro'yxatdan o'tish uchun ma'lumotlaringizni kiriting!"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        new_user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        new_user.set_password(validated_data['password'])
        new_user.save()

        return redirect('rest_framework:login')


class LocationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = LocationUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Location updated successfully'})
        return Response(serializer.errors, status=400)


class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('id_token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            return Response({"message": "Successfully logged in"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
