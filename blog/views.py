from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Tag, CustomUser


class PostsView(APIView):
    class PostSerializer(serializers.ModelSerializer):
        class CommentSerializer(serializers.ModelSerializer):
            class Meta:
                model = Comment
                fields = "__all__"

        class TagSerializer(serializers.ModelSerializer):
            class Meta:
                model = Tag
                fields = "__all__"

        class AuthorSerializer(serializers.ModelSerializer):
            class Meta:
                model = CustomUser
                fields = ["username", "email", "phone_number"]

        # comments = CommentSerializer(many=True)
        tags = TagSerializer(many=True)
        author = AuthorSerializer()

        class Meta:
            model = Post
            fields = ["title", "created_at", "comments_count", "tags", "author", "content"]

    @method_decorator(cache_page(60))
    def get(self, request):
        posts = Post.objects.select_related("author").prefetch_related(
            Prefetch("tags", queryset=Tag.objects.all()),
        ).all()

        serializer = self.PostSerializer(posts, many=True)

        return Response(serializer.data)
