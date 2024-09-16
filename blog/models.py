from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from blog.utils import cache_decorator


class CustomUser(User):
    bio = models.TextField(max_length=1000, verbose_name="Bio", blank=True, null=True)
    phone_number = models.CharField(verbose_name="phone number", max_length=20,
                                    validators=[RegexValidator(r'^\+7\d{10}$')], blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["phone_number"])
        ]


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    tags = models.ManyToManyField("Tag", verbose_name="tags", related_name="posts")

    @property
    @cache_decorator()
    def comments_count(self) -> int:
        return self.comments.count()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["created_at", "author_id"]),
        ]


class Tag(models.Model):
    title = models.CharField(max_length=150, verbose_name="Title")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["slug"])
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post", related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Author")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["post", "author"])
        ]
