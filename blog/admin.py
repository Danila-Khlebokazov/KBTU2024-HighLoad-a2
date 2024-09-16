from django.contrib import admin

from .models import Post, Comment, Tag, CustomUser

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(CustomUser)
