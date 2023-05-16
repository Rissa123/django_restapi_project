from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class OverviewAPI(generics.ListAPIView):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user)


class CreateAPI(generics.CreateAPIView):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tags_data = serializer.validated_data.pop('tags')
        tags = []
        for tag_data in tags_data:
            title = tag_data['title']
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        serializer.save(user=self.request.user, tags=tags)


class DetailAPI(generics.RetrieveAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        tags_data = serializer.validated_data.pop('tags')
        tags = []
        for tag_data in tags_data:
            title = tag_data['title']
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        instance = serializer.save(tags=tags)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DeleteAPI(generics.DestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


