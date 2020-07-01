from django.contrib import admin
from .models import Message, Post, Comment
# Register your models here.
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Comment)

