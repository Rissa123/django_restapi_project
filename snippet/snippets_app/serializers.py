from rest_framework import serializers
from .models import Tag, Snippet

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']

class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'content', 'timestamp', 'user', 'tags']
        read_only_fields = ['id', 'timestamp', 'user']